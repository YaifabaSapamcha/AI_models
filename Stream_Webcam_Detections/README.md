# 👁️ Person Detection Stream

A **Raspberry Pi optimized** real-time webcam streaming application with **YOLOv5 person detection**. Stream directly in your browser or VLC player - no templates, just pure video with person detection overlay.

## ✨ Features

- 👥 **Person detection ONLY** - focused and efficient
- 🍓 **Raspberry Pi optimized** - runs great on Pi Zero to Pi 4
- 📹 **Direct video stream** at root path `/` - no web UI needed
- 🎬 **VLC compatible** MJPEG streaming
- 📱 **Access from any device** on your network
- ⚡ **Performance optimized** - lower CPU usage, configurable quality
- 🎯 **Person counting** - real-time count overlay
- 📡 **REST API** for person detection data
- 🏠 **Local network only** - works offline, privacy-focused

## 🚀 Quick Start

### Raspberry Pi (Recommended)
```bash
# Clone the project
git clone <repository-url>
cd webcam-object-detection-stream

# Run the Pi-optimized setup
chmod +x setup-pi.sh
./setup-pi.sh

# Start streaming
./run.sh
```

> 📖 **For complete Raspberry Pi guide, see:** [README-PI.md](README-PI.md)

### Other Systems (Windows/macOS/Linux)
```bash
# Clone the project
git clone <repository-url>
cd webcam-object-detection-stream

# Choose installation method:

# Option 1: Full installation (recommended)
pip install -r requirements.txt

# Option 2: Minimal installation (streaming only, no detection)
pip install -r requirements-minimal.txt

# Start streaming
python app.py
```

### Dell Inspiron 15 3511

For the Windows laptop profile, use the conservative 640×480 / 10 FPS settings and the shared camera worker:

```powershell
Copy-Item .env.example .env
Set-ExecutionPolicy -Scope Process Bypass
.\run.ps1
```

Open `http://127.0.0.1:8080/`. Detection is off by default so the stream starts smoothly on the integrated CPU; enable it from the dashboard when needed. See [README-DELL.md](README-DELL.md) for troubleshooting and network access.

### Access the Stream

Once running, access from any device on the same network:

- **📹 Direct Stream:** `http://<pi-ip>:8080/` (opens directly in browser)
- **🎬 VLC Stream:** `http://<pi-ip>:8080/stream`  
- **👥 Person API:** `http://<pi-ip>:8080/api/persons`
- **❤️ Health Check:** `http://<pi-ip>:8080/healthz`

> **Find Pi IP:** Run `hostname -I` on Raspberry Pi

## 📦 Requirements Files

Choose the right requirements file for your setup:

### 📜 **requirements.txt** (Standard)
- **For:** Desktop/laptop, full features
- **Includes:** Full PyTorch, all dependencies
- **Size:** ~2GB download
- **Features:** Person detection, all optimizations

### 🍓 **requirements-pi.txt** (Raspberry Pi)
- **For:** Raspberry Pi (all models)
- **Includes:** CPU-only PyTorch, Pi optimizations
- **Size:** ~500MB download (much smaller)
- **Features:** Person detection optimized for Pi
- **Auto-used:** by `setup-pi.sh` and `run.sh` on Pi

### ⚡ **requirements-minimal.txt** (Testing)
- **For:** Quick testing, streaming only
- **Includes:** Basic Flask + OpenCV
- **Size:** ~50MB download
- **Features:** Camera streaming only (no detection)
- **Use case:** Test camera before installing ML dependencies

```bash
# Examples:
pip install -r requirements.txt         # Full installation
pip install -r requirements-pi.txt      # Pi optimized
pip install -r requirements-minimal.txt # Minimal streaming
```

## 📋 System Requirements

### System Requirements
- **Python 3.8+**
- **Webcam** (built-in or USB)
- **4GB+ RAM** (recommended for YOLO models)
- **Modern CPU** (GPU optional but recommended for better performance)

### Supported Platforms
- ✅ Windows 10/11
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu, Debian, CentOS, etc.)
- ✅ Raspberry Pi OS (4GB+ model recommended)

## ⚙️ Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

### Key Settings

```env
# Server Configuration
HOST=0.0.0.0          # Listen on all interfaces
PORT=8080              # Port number

# Camera Settings
CAMERA_INDEX=0         # Webcam index (0 = default)
WIDTH=1280             # Video width
HEIGHT=720             # Video height  
FPS=15                 # Target frames per second

# Object Detection
DETECTION_ENABLED=true # Enable/disable detection
DETECTION_MODEL=yolov5s # Model size: yolov5n, yolov5s, yolov5m, yolov5l, yolov5x

# Performance
JPEG_QUALITY=80        # Stream quality (1-100)
CONFIDENCE_THRESHOLD=0.5 # Detection confidence threshold
```

### Model Performance Guide

| Model | Speed | Accuracy | RAM Usage | Best For |
|-------|--------|----------|-----------|----------|
| `yolov5n` | ⚡⚡⚡⚡ | ⭐⭐ | ~1GB | Raspberry Pi, Low-end |
| `yolov5s` | ⚡⚡⚡ | ⭐⭐⭐ | ~2GB | Default, Balanced |
| `yolov5m` | ⚡⚡ | ⭐⭐⭐⭐ | ~4GB | Better accuracy |
| `yolov5l` | ⚡ | ⭐⭐⭐⭐⭐ | ~6GB | High accuracy |
| `yolov5x` | ⚡ | ⭐⭐⭐⭐⭐ | ~8GB | Maximum accuracy |

## 🎮 Usage

### Web Interface Features

1. **Live Video Stream** - Real-time webcam feed with detection overlays
2. **Detection Toggle** - Enable/disable object detection on-the-fly
3. **Live Statistics** - FPS, object count, uptime tracking
4. **Stream Controls** - Refresh stream, view direct feeds
5. **Detection List** - Real-time list of detected objects with confidence scores

### VLC Access

1. Open VLC Media Player
2. Go to `Media` → `Open Network Stream`
3. Enter: `http://<your-ip>:8080/stream.mjpg`
4. Click Play

### API Endpoints

- `GET /` - Web interface
- `GET /video_feed` - MJPEG stream for browsers
- `GET /stream.mjpg` - MJPEG stream for VLC
- `GET /api/detections` - Current detections as JSON
- `GET /api/stats` - Performance statistics
- `POST /api/toggle_detection` - Toggle detection on/off
- `GET /healthz` - Health check
- `GET /about` - Application information

### API Response Example

```json
{
  "detections": [
    {
      "class": "person",
      "confidence": 0.87,
      "bbox": [245, 123, 456, 678]
    },
    {
      "class": "laptop", 
      "confidence": 0.92,
      "bbox": [100, 200, 300, 400]
    }
  ],
  "stats": {
    "fps": 12.5,
    "detection_count": 2,
    "frame_count": 1547
  },
  "timestamp": 1674123456.789
}
```

## 🔧 Installation Details

### Manual Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd webcam-object-detection-stream
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure settings (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

### Raspberry Pi Specific Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
sudo apt install -y python3-pip python3-venv python3-dev

# Install camera utilities (optional)
sudo apt install -y v4l-utils

# Check camera
v4l2-ctl --list-devices

# Clone and setup
git clone <repository-url>
cd webcam-object-detection-stream
chmod +x run.sh
./run.sh
```

### GPU Acceleration (Optional)

For NVIDIA GPUs, install CUDA-enabled PyTorch:

```bash
# Replace CPU version in requirements.txt with:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## 🌐 Network Access

### Same Network Access
- Ensure your device and client are on the same Wi-Fi/router
- Use the device's local IP address (e.g., `192.168.1.100:8080`)
- No internet connection required

### Remote Access (Advanced)
For access from outside your network, consider:

1. **VPN** (Recommended) - Use Tailscale, WireGuard, or OpenVPN
2. **Reverse Proxy** - Use Caddy/Nginx with authentication
3. **Port Forwarding** - Configure router (not recommended without auth)

⚠️ **Security Warning:** This application has no built-in authentication. Do not expose directly to the internet without proper security measures.

## 🐛 Troubleshooting

### Common Issues

**Camera not detected**
```bash
# Linux: Check available cameras
ls -l /dev/video*
v4l2-ctl --list-devices

# Windows: Try different CAMERA_INDEX values (0, 1, 2...)
```

**Model loading fails**
- Check internet connection (first run downloads model)
- Ensure sufficient RAM for chosen model
- Try smaller model (yolov5n) for limited hardware

**Poor performance**
- Lower resolution in `.env` (e.g., 640x480)
- Reduce FPS target
- Use smaller YOLO model
- Disable detection temporarily

**Stream not loading in browser**
- Check firewall settings
- Try different port in `.env`
- Refresh browser/clear cache
- Check application logs

**VLC can't connect**
- Ensure VLC network caching is enabled
- Try direct IP instead of hostname
- Check network firewall rules

### Performance Optimization

**For Raspberry Pi:**
```env
# Lighter settings for Pi
WIDTH=640
HEIGHT=480
FPS=10
DETECTION_MODEL=yolov5n
JPEG_QUALITY=60
```

**For desktop/server:**
```env
# Higher quality settings
WIDTH=1920
HEIGHT=1080
FPS=30
DETECTION_MODEL=yolov5m
JPEG_QUALITY=90
```

## 📝 Detected Object Classes

YOLOv5 can detect 80 different object classes including:

**People & Animals:** person, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe

**Vehicles:** bicycle, car, motorcycle, airplane, bus, train, truck, boat

**Indoor Objects:** chair, sofa, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush

**Sports:** frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket

And many more! See the full list in the YOLO documentation.

## 🤝 Contributing

Contributions are welcome! Please feel free to:

- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **YOLOv5** by Ultralytics for object detection
- **OpenCV** for computer vision processing  
- **Flask** for the web framework
- **PyTorch** for deep learning inference

---

**Made with ❤️ for the maker community**

*Perfect for security monitoring, educational projects, IoT applications, and more!*
