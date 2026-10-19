# Webcam Detection Stream

A lightweight local webcam streaming application with optional real-time person detection. It captures video with OpenCV, serves an MJPEG stream through Flask, and can use a YOLOv5 nano model to detect people.

The application is designed to work well on CPU-only laptops such as the **Dell Inspiron 15 3511**, as well as Linux systems and Raspberry Pi devices.

## Features

- Live webcam streaming in Chrome, Edge, Firefox, or VLC
- Optional person-only detection using YOLOv5 nano
- Responsive browser dashboard
- Shared camera worker for multiple viewers
- Camera retry handling when the webcam is unavailable or busy
- Live FPS, frame count, uptime, camera status, and detection status
- REST API for detection data, statistics, and health checks
- Configurable camera index, resolution, FPS, JPEG quality, and detection interval
- Local-network operation without an external streaming service

## Project structure

```text
Stream_Webcam_Detections/
├── app.py                  # Flask application and camera worker
├── templates/
│   └── index.html          # Browser dashboard
├── static/
│   └── style.css           # Dashboard styling
├── yolov5n.pt              # Local YOLOv5 nano model
├── .env.example            # Configuration template
├── requirements.txt        # Full dependencies with detection support
├── requirements-minimal.txt# Streaming-only dependencies
├── run.ps1                 # Windows setup and launcher
├── run.sh                  # Linux setup and launcher
└── README.md               # Current file
```

## Requirements

### Hardware

- Built-in or USB webcam
- At least 4 GB RAM recommended for person detection
- Modern CPU
- Windows 10/11, Linux, macOS, or Raspberry Pi OS

### Software

- Python 3.9 or newer recommended
- Internet connection for the first dependency installation
- A modern browser for viewing the dashboard

## Quick start on Windows

This setup was build for my Dell Inspiron 15 3511. But it should work on similar laptops or pc.

Open PowerShell in the project directory:

```powershell
cd "D:\path\to\Stream_Webcam_Detections"
```

Create the configuration file:

```powershell
Copy-Item .env.example .env
```

Allow local script execution for the current PowerShell session:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Start the application:

```powershell
.\run.ps1
```

Open the dashboard:

```text
http://127.0.0.1:8080/
```

The Windows launcher creates a virtual environment, installs dependencies, loads `.env`, and starts the application.

### Manual Windows setup

If you prefer to run each step manually:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.venv\Scripts\python.exe app.py
```

## Quick start on Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Alternatively, use the launcher on Linux:

```bash
chmod +x run.sh
./run.sh
```

Open:

```text
http://127.0.0.1:8080/
```

## Streaming-only installation

If you only need webcam streaming and do not need person detection, install the smaller dependency set:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-minimal.txt
$env:DETECTION_ENABLED="false"
.venv\Scripts\python.exe app.py
```

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-minimal.txt
DETECTION_ENABLED=false python app.py
```

Streaming-only mode is recommended when the main priority is the smoothest possible video stream on a low-power CPU.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed:

```env
HOST=0.0.0.0
PORT=8080

CAMERA_INDEX=0
WIDTH=640
HEIGHT=480
FPS=10
JPEG_QUALITY=70

DETECTION_ENABLED=false
DETECTION_MODEL=yolov5n
CONFIDENCE_THRESHOLD=0.50
DETECTION_SIZE=320
DETECTION_INTERVAL=3
TORCH_THREADS=2
```

### Configuration reference

| Variable | Default | Description |
|---|---:|---|
| `HOST` | `0.0.0.0` | Network interface used by the server |
| `PORT` | `8080` | HTTP port |
| `CAMERA_INDEX` | `0` | Webcam index; try `1` if the default camera is not found |
| `WIDTH` | `640` | Stream width in pixels |
| `HEIGHT` | `480` | Stream height in pixels |
| `FPS` | `10` | Target capture and stream frame rate |
| `JPEG_QUALITY` | `70` | JPEG quality from 30 to 95 |
| `DETECTION_ENABLED` | `false` | Enable or disable person detection at startup |
| `DETECTION_MODEL` | `yolov5n` | Detection model name or fallback model source |
| `CONFIDENCE_THRESHOLD` | `0.50` | Minimum detection confidence |
| `DETECTION_SIZE` | `320` | YOLO inference size; lower values use less CPU |
| `DETECTION_INTERVAL` | `3` | Run detection every Nth frame |
| `TORCH_THREADS` | `2` | CPU threads reserved for PyTorch inference |

## Dell Inspiron 15 3511 recommended settings

For smooth webcam streaming:

```env
WIDTH=640
HEIGHT=480
FPS=10
JPEG_QUALITY=70
DETECTION_ENABLED=false
```

For optional detection while limiting CPU usage:

```env
WIDTH=640
HEIGHT=480
FPS=10
DETECTION_ENABLED=true
DETECTION_SIZE=320
DETECTION_INTERVAL=3
TORCH_THREADS=2
```

If detection is too slow, increase `DETECTION_INTERVAL` to `5` or `8`, reduce `DETECTION_SIZE` to `256`, or turn detection off.

If the stream itself is slow, use:

```env
WIDTH=480
HEIGHT=360
FPS=8
JPEG_QUALITY=60
DETECTION_ENABLED=false
```

## Accessing the stream

### Browser dashboard

```text
http://127.0.0.1:8080/
```

### MJPEG stream

```text
http://127.0.0.1:8080/stream
```

Additional stream aliases:

```text
http://127.0.0.1:8080/video_feed
http://127.0.0.1:8080/video
http://127.0.0.1:8080/stream.mjpg
```

### VLC

1. Open VLC Media Player.
2. Select **Media → Open Network Stream**.
3. Enter:

```text
http://127.0.0.1:8080/stream.mjpg
```

4. Select **Play**.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Browser dashboard |
| `GET` | `/stream` | MJPEG stream |
| `GET` | `/api/persons` | Current person detections |
| `GET` | `/api/detections` | Alias for the detection API |
| `GET` | `/api/stats` | FPS, uptime, and frame statistics |
| `POST` | `/api/toggle_detection` | Enable or disable detection |
| `GET` | `/healthz` | Camera and model health information |
| `GET` | `/info` | Application information |

Example:

```text
http://127.0.0.1:8080/healthz
```

Example detection response:

```json
{
  "persons": [
    {
      "class": "person",
      "confidence": 0.87,
      "bbox": [245, 123, 456, 678],
      "id": 1
    }
  ],
  "person_count": 1,
  "timestamp": 1730000000.0
}
```

## Access from another device on the same Wi-Fi

1. Start the server on the laptop.
2. In PowerShell, find the laptop's IP address:

```powershell
ipconfig
```

3. Find the IPv4 address of the active Wi-Fi adapter, for example `192.168.1.25`.
4. Allow Python through Windows Firewall when Windows asks. Choose **Private networks** only.
5. From another device on the same network, open:

```text
http://192.168.1.25:8080/
```

Do not expose this application directly to the public internet. It does not include authentication.

## Troubleshooting

### PowerShell reports errors near `from app import create_app`

This means PowerShell is trying to interpret Python code as PowerShell code. Use the corrected `run.ps1` from this project and start it with:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\run.ps1
```

The launcher should not contain an embedded `python -c @" ... "@` block.

### Camera not found

Try these steps:

1. Close Camera, Teams, Zoom, OBS, or other programs using the webcam.
2. Try another camera index in `.env`:

```env
CAMERA_INDEX=1
```

3. Restart the application.
4. Check Windows **Settings → Privacy & security → Camera** and enable camera access for desktop applications.

### Stream is slow

Lower the workload:

```env
WIDTH=480
HEIGHT=360
FPS=8
JPEG_QUALITY=60
DETECTION_ENABLED=false
```

If detection is enabled, increase `DETECTION_INTERVAL` or reduce `DETECTION_SIZE`.

### Detection model does not load

The webcam stream should still work without the model. Check that the full dependencies are installed:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

For streaming without detection, set:

```env
DETECTION_ENABLED=false
```

### Port 8080 is already in use

Change the port in `.env`:

```env
PORT=8090
```

Then open:

```text
http://127.0.0.1:8090/
```

### Browser shows a blank stream

Check the health endpoint:

```text
http://127.0.0.1:8080/healthz
```

Also try the direct stream:

```text
http://127.0.0.1:8080/stream
```

## Privacy and security

The camera feed is processed locally by default. The application does not upload frames to an external service.

However, the server has no built-in authentication. Use it only on a trusted local network, or place it behind a VPN and authenticated reverse proxy before exposing it to other networks.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).
