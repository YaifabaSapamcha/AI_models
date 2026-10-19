"""Person and object detection using Ultralytics YOLO.

This module intentionally contains no face-recognition code.

The default yolo11n.pt model is trained on COCO. It can detect common classes
such as person, bicycle, car, bottle, laptop, and book. It cannot reliably
detect pen, juice box, or spectacles unless you provide a custom YOLO model
trained for those classes with --model.
"""

import argparse
from collections import defaultdict

import cv2
from ultralytics import YOLO

# COCO names are converted to the names requested by the application.
DISPLAY_ALIASES = {
    "person": "person",
    "bicycle": "bike",
    "car": "car",
    "bottle": "bottle",
    "laptop": "laptop",
    "book": "book",
    # These names work when supplied by a custom model.
    "pen": "pen",
    "juice box": "juice box",
    "juice_box": "juice box",
    "spectacle": "spectacle",
    "spectacles": "spectacle",
    "glasses": "spectacle",
}

# Only these requested categories are shown. Add another model class here if
# you want it displayed after training or supplying a custom YOLO model.
REQUESTED_CLASSES = {
    "person", "bicycle", "car", "bottle", "laptop", "book",
    "pen", "juice box", "juice_box", "spectacle", "spectacles", "glasses",
}


def normalise_name(name):
    return " ".join(str(name).strip().lower().replace("_", " ").split())


def display_name(name):
    normalised = normalise_name(name)
    return DISPLAY_ALIASES.get(normalised, normalised)


def is_requested_class(name):
    normalised = normalise_name(name)
    return normalised in {normalise_name(x) for x in REQUESTED_CLASSES}


def person_label(track_id, person_numbers):
    """Give each tracked person a stable number during this camera session."""
    if track_id not in person_numbers:
        person_numbers[track_id] = len(person_numbers) + 1
    return f"person {number_word(person_numbers[track_id])}"


def number_word(number):
    words = {
        1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
        6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
    }
    return words.get(number, str(number))


def object_label(name, occurrence):
    """Number repeated object classes independently in each processed frame."""
    label = display_name(name)
    return f"{label} {number_word(occurrence)}"


def detect(camera_index=0, width=640, height=480, confidence=0.45,
           image_size=320, process_every=2, model_path="yolo11n.pt"):
    model = YOLO(model_path)
    camera = cv2.VideoCapture(camera_index)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not camera.isOpened():
        raise RuntimeError("Could not open the camera")

    # track_id -> assigned person number; IDs are stable while the tracker can
    # follow the person. They reset when the program exits.
    person_numbers = {}
    last_detections = []
    frame_number = 0

    print("Detecting persons and requested objects. Press q to quit.")
    print("Person numbers reset when the program exits.")

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                print("Could not read a camera frame")
                break

            frame_number += 1
            if frame_number % max(1, process_every) == 0:
                last_detections = []
                object_counts = defaultdict(int)

                # ByteTrack keeps person IDs steadier than assigning numbers
                # independently on every frame. Only CPU inference is used.
                results = model.track(
                    source=frame,
                    persist=True,
                    tracker="bytetrack.yaml",
                    imgsz=image_size,
                    conf=confidence,
                    device="cpu",
                    verbose=False,
                )
                result = results[0]

                if result.boxes is not None:
                    names = result.names
                    for box, class_id, track_id in zip(
                        result.boxes.xyxy.cpu().numpy(),
                        result.boxes.cls.cpu().numpy().astype(int),
                        (result.boxes.id.int().cpu().tolist()
                         if result.boxes.id is not None
                         else [None] * len(result.boxes)),
                    ):
                        raw_name = normalise_name(names[int(class_id)])
                        if not is_requested_class(raw_name):
                            continue

                        x1, y1, x2, y2 = map(int, box)
                        if raw_name == "person":
                            # A missing tracker ID is unusual, but still gets
                            # a deterministic temporary number for this box.
                            track_key = ("untracked", x1, y1, x2, y2) if track_id is None else int(track_id)
                            label = person_label(track_key, person_numbers)
                            color = (0, 200, 0)  # green
                        else:
                            object_counts[display_name(raw_name)] += 1
                            label = object_label(
                                raw_name, object_counts[display_name(raw_name)]
                            )
                            color = (255, 130, 0)  # blue, BGR

                        last_detections.append(((x1, y1, x2, y2), label, color))

            for (x1, y1, x2, y2), label, color in last_detections:
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                text_y = max(22, y1 - 8)
                cv2.putText(frame, label, (x1, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.60, color, 2,
                            cv2.LINE_AA)

            cv2.imshow("Person and object detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        description="Detect persons and selected objects; no face recognition."
    )
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--confidence", type=float, default=0.45)
    parser.add_argument("--image-size", type=int, default=320,
                        help="Use 256 or 320 for better CPU performance")
    parser.add_argument("--process-every", type=int, default=2,
                        help="Run detection every N frames")
    parser.add_argument("--model", default="yolo11n.pt",
                        help="YOLO model; use a custom .pt for pen/juice box/spectacle")
    args = parser.parse_args()

    detect(
        camera_index=args.camera,
        width=args.width,
        height=args.height,
        confidence=args.confidence,
        image_size=args.image_size,
        process_every=args.process_every,
        model_path=args.model,
    )


if __name__ == "__main__":
    main()
