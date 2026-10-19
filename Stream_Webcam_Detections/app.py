import os
import threading
import time
from typing import Generator, List, Optional, Tuple

import cv2
import numpy as np
from flask import Flask, Response, jsonify, render_template, request

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False


def env(key: str, default: str) -> str:
    value = os.getenv(key)
    return default if value is None or value == "" else value


def int_env(key: str, default: int) -> int:
    try:
        return int(env(key, str(default)).split("#", 1)[0].strip())
    except (TypeError, ValueError):
        return default


def float_env(key: str, default: float) -> float:
    try:
        return float(env(key, str(default)).split("#", 1)[0].strip())
    except (TypeError, ValueError):
        return default


def bool_env(key: str, default: bool) -> bool:
    return env(key, str(default)).split("#", 1)[0].lower().strip() in {"1", "true", "yes", "on"}


class PersonDetector:
    """Small, lazy-loaded CPU detector. Streaming remains available if ML loading fails."""

    def __init__(self) -> None:
        self.model = None
        self.enabled = bool_env("DETECTION_ENABLED", False)
        self.confidence_threshold = max(0.05, min(0.99, float_env("CONFIDENCE_THRESHOLD", 0.5)))
        self.inference_size = int_env("DETECTION_SIZE", 320)
        self.model_name = env("DETECTION_MODEL", "yolov5n")
        self.status = "disabled" if not self.enabled else "loading"
        self.error = ""
        self._load_lock = threading.Lock()

    def load(self) -> None:
        if not self.enabled or self.model is not None:
            return
        with self._load_lock:
            if self.model is not None or not self.enabled:
                return
            try:
                if not ULTRALYTICS_AVAILABLE:
                    raise RuntimeError("ultralytics is not installed")
                model_path = os.path.join(os.path.dirname(__file__), "yolov5n.pt")
                source = model_path if os.path.exists(model_path) else self.model_name
                print(f"Loading {source} on CPU (streaming stays available during startup)...")
                self.model = YOLO(source)
                if TORCH_AVAILABLE:
                    torch.set_num_threads(max(1, int_env("TORCH_THREADS", 2)))
                self.status = "ready"
                print("Person detector ready")
            except Exception as exc:
                self.error = str(exc)
                self.status = "error"
                self.model = None
                print(f"Person detector unavailable: {exc}")

    def detect(self, frame: np.ndarray) -> Tuple[np.ndarray, List[dict]]:
        if not self.enabled:
            return frame, []
        if self.model is None:
            self.load()
        if self.model is None:
            return frame, []

        try:
            result = self.model.predict(
                source=frame,
                imgsz=self.inference_size,
                conf=self.confidence_threshold,
                classes=[0],
                device="cpu",
                verbose=False,
            )[0]
            detections: List[dict] = []
            for index, (box, confidence) in enumerate(
                zip(result.boxes.xyxy.cpu().numpy(), result.boxes.conf.cpu().numpy()), start=1
            ):
                x1, y1, x2, y2 = [int(value) for value in box]
                confidence = float(confidence)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 220, 80), 2)
                label = f"Person #{index}: {confidence:.2f}"
                text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)[0]
                top = max(0, y1 - text_size[1] - 8)
                cv2.rectangle(frame, (x1, top), (x1 + text_size[0] + 4, y1), (0, 220, 80), -1)
                cv2.putText(frame, label, (x1 + 2, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)
                detections.append({
                    "class": "person",
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2],
                    "id": index,
                })
            if detections:
                cv2.putText(frame, f"Persons: {len(detections)}", (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 80), 2)
            return frame, detections
        except Exception as exc:
            self.error = str(exc)
            self.status = "error"
            print(f"Person detection error: {exc}")
            return frame, []


class FrameHub:
    """Owns the camera and publishes one latest JPEG to every browser/VLC client."""

    def __init__(self, detector: PersonDetector) -> None:
        self.camera_index = int_env("CAMERA_INDEX", 0)
        self.width = int_env("WIDTH", 640)
        self.height = int_env("HEIGHT", 480)
        self.fps = max(1, int_env("FPS", 10))
        self.jpeg_quality = max(30, min(95, int_env("JPEG_QUALITY", 70)))
        self.detection_interval = max(1, int_env("DETECTION_INTERVAL", 3))
        self.detector = detector
        self.lock = threading.Condition()
        self.latest_jpeg: Optional[bytes] = None
        self.latest_detections: List[dict] = []
        self.sequence = 0
        self.camera_ok = False
        self.running = True
        self.stats = {"fps": 0.0, "frame_count": 0, "detection_fps": 0.0, "started_at": time.time()}
        self._thread = threading.Thread(target=self._run, name="camera-worker", daemon=True)
        self._thread.start()

    def _open_camera(self) -> Optional[cv2.VideoCapture]:
        cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY)
        if not cap.isOpened():
            cap.release()
            return None
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        cap.set(cv2.CAP_PROP_FPS, self.fps)
        # Keep camera buffering small so a slow detector never shows stale video.
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        return cap

    def _run(self) -> None:
        cap: Optional[cv2.VideoCapture] = None
        frame_number = 0
        last_tick = time.monotonic()
        frames_at_tick = 0
        while self.running:
            if cap is None or not cap.isOpened():
                cap = self._open_camera()
                self.camera_ok = cap is not None
                if cap is None:
                    time.sleep(2)
                    continue
                print(f"Camera {self.camera_index} ready at up to {self.width}x{self.height}@{self.fps}fps")

            ok, frame = cap.read()
            if not ok or frame is None:
                self.camera_ok = False
                cap.release()
                cap = None
                time.sleep(0.5)
                continue

            actual_height, actual_width = frame.shape[:2]
            if actual_width != self.width or actual_height != self.height:
                frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_AREA)
            frame_number += 1

            if self.detector.enabled and frame_number % self.detection_interval == 0:
                frame, detections = self.detector.detect(frame)
                self.latest_detections = detections
            elif self.latest_detections:
                # Keep the last boxes visible between detector runs for a stable overlay.
                detections = self.latest_detections
            else:
                detections = []

            success, encoded = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality])
            if not success:
                continue

            now = time.monotonic()
            elapsed = now - last_tick
            if elapsed >= 1.0:
                self.stats["fps"] = (frame_number - frames_at_tick) / elapsed
                frames_at_tick = frame_number
                last_tick = now
            self.stats["frame_count"] += 1
            with self.lock:
                self.latest_jpeg = encoded.tobytes()
                self.sequence += 1
                self.stats["person_count"] = len(detections)
                self.lock.notify_all()
            time.sleep(max(0.0, (1.0 / self.fps) - (time.monotonic() - now)))

        if cap is not None:
            cap.release()

    def frames(self) -> Generator[bytes, None, None]:
        last_sequence = -1
        while self.running:
            with self.lock:
                self.lock.wait_for(lambda: self.latest_jpeg is not None and self.sequence != last_sequence, timeout=2.0)
                jpeg = self.latest_jpeg
                last_sequence = self.sequence
            if jpeg is None:
                continue
            yield b"--frame\r\nContent-Type: image/jpeg\r\nCache-Control: no-cache\r\n\r\n" + jpeg + b"\r\n"

    def snapshot(self) -> dict:
        with self.lock:
            stats = dict(self.stats)
            stats["uptime"] = round(time.time() - stats.pop("started_at"), 1)
            stats["person_count"] = len(self.latest_detections)
            return stats


def create_app() -> Flask:
    app = Flask(__name__)
    detector = PersonDetector()
    hub = FrameHub(detector)

    @app.route("/")
    def dashboard():
        return render_template(
            "index.html",
            detection_enabled=detector.enabled,
            model_loaded=detector.status == "ready",
            width=hub.width,
            height=hub.height,
            fps=hub.fps,
        )

    @app.route("/stream")
    @app.route("/video")
    @app.route("/video_feed")
    @app.route("/stream.mjpg")
    def video_feed():
        return Response(hub.frames(), mimetype="multipart/x-mixed-replace; boundary=frame", headers={"Cache-Control": "no-store"})

    @app.route("/raw")
    def raw_stream():
        return video_feed()

    @app.route("/api/persons")
    @app.route("/api/detections")
    def api_persons():
        detections = list(hub.latest_detections)
        return jsonify({"persons": detections, "detections": detections, "person_count": len(detections), "stats": hub.snapshot(), "timestamp": time.time()})

    @app.post("/api/toggle_detection")
    def toggle_detection():
        detector.enabled = not detector.enabled
        detector.status = "loading" if detector.enabled else "disabled"
        return jsonify({"detection_enabled": detector.enabled, "message": "Detection enabled" if detector.enabled else "Detection disabled"})

    @app.get("/api/stats")
    def api_stats():
        return jsonify(hub.snapshot())

    @app.get("/healthz")
    def health():
        return jsonify({"status": "ok" if hub.camera_ok else "waiting_for_camera", "camera": hub.camera_ok, "person_detection_model": detector.model is not None, "detection_status": detector.status, "detection_enabled": detector.enabled, "current_persons": len(hub.latest_detections), "error": detector.error})

    @app.get("/info")
    def info():
        return jsonify({"name": "Person Detection Stream", "version": "3.0.0", "optimized_for": ["Dell Inspiron 15 3511", "CPU-only laptops"], "endpoints": {"dashboard": "/", "mjpeg": "/stream", "person_api": "/api/persons", "stats_api": "/api/stats", "health": "/healthz"}})

    return app


if __name__ == "__main__":
    app = create_app()
    host = env("HOST", "0.0.0.0")
    port = int_env("PORT", 8080)
    print(f"Person Detection Stream: http://127.0.0.1:{port}/")
    app.run(host=host, port=port, debug=False, threaded=True)
