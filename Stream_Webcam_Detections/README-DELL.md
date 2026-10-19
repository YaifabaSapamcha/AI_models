# Dell Inspiron 15 3511 setup

This profile favors a stable webcam stream over maximum AI detection speed. The application uses one background camera worker and shares the latest JPEG with all browser/VLC clients, so opening the dashboard does not start multiple competing camera readers.

## Windows setup

Open PowerShell in this folder:

```powershell
Copy-Item .env.example .env
Set-ExecutionPolicy -Scope Process Bypass
.\run.ps1
```

Open `http://127.0.0.1:8080/` in Chrome or Edge. If the webcam is not found, close Teams/Zoom/Camera and try `CAMERA_INDEX=1` in `.env`.

The default profile is 640×480 at 10 FPS with detection off. Click **Enable detection** only when needed. For a smoother stream, keep detection off; for detection with lower CPU use, keep `DETECTION_INTERVAL=3` or increase it to `5`.

## Working URLs

- Dashboard: `http://127.0.0.1:8080/`
- MJPEG stream: `http://127.0.0.1:8080/stream`
- VLC-compatible alias: `http://127.0.0.1:8080/stream.mjpg`
- Detection JSON: `http://127.0.0.1:8080/api/persons`
- Health: `http://127.0.0.1:8080/healthz`

To view from another device on the same Wi-Fi, find the laptop's IPv4 address with `ipconfig`, allow Python through Windows Firewall on Private networks, and open `http://<laptop-ip>:8080/` from the other device. Do not expose this unauthenticated server directly to the public internet.

## If installation is too large

For webcam-only streaming, install the smaller dependency set and run with detection disabled:

```powershell
.venv\\Scripts\\python -m pip install -r requirements-minimal.txt
$env:DETECTION_ENABLED="false"
.venv\\Scripts\\python app.py
```

The full `requirements.txt` is needed for the optional YOLO person detector.
