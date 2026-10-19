# 🍓 Raspberry Pi Person Detection Stream

**Complete guide for running person detection streaming on Raspberry Pi**

📦 **Standalone ZIP Distribution** - Everything included, no git required!

A lightweight, **person-only detection** system optimized specifically for Raspberry Pi. Stream your Pi camera with real-time person detection to any device on your network.

---

## 📦 Installation from ZIP

**Prerequisites:** You have already extracted the zip file to your Raspberry Pi.

1. **Transfer the zip file to your Pi:**
   ```bash
   # Via USB, SCP, or download directly on Pi
   # Example: scp webcam-detection-stream.zip pi@your-pi-ip:~/
   ```

2. **Extract on Raspberry Pi:**
   ```bash
   unzip webcam-detection-stream.zip
   cd webcam-object-detection-stream
   ```

3. **Ready to run!** 🚀

---

## 🚀 Quick Start (One Command)

```bash
# Extract and run
cd webcam-object-detection-stream
chmod +x setup-pi.sh
./setup-pi.sh
```

**That's it!** The script will:
- ✅ Detect your Pi model and optimize settings
- ✅ Install all dependencies (CPU-only PyTorch)
- ✅ Set up virtual environment
- ✅ Test your camera
- ✅ Start the person detection stream

---

## 📋 Requirements

### Hardware
- **Raspberry Pi** (Any model - Zero, 3, 4, 5)
- **Camera** (Pi Camera Module or USB webcam)
- **8GB+ SD Card** (16GB+ recommended)
- **Stable power supply**

### Software  
- **Raspberry Pi OS** (Bookworm/Bullseye)
- **Python 3.8+** (pre-installed)
- **Internet connection** (for initial setup only)

---

## 🛠️ Manual Setup

**Note:** The zip file contains all source code - no git required!

### Step 1: Enable Camera
```bash
sudo raspi-config
# Navigate to: Interface Options → Camera → Enable
sudo reboot
```

### Step 2: System Updates
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv python3-dev v4l-utils
```

### Step 3: Navigate to Project Directory
```bash
cd webcam-object-detection-stream  # From extracted zip
```

### Step 4: Run Setup Script
```bash
chmod +x setup-pi.sh
./setup-pi.sh
```

---

## 🎛️ Pi Model Optimizations

The setup script **automatically detects** your Pi model and applies optimal settings:

### Pi Zero / Pi 1
```bash
# Optimized settings applied automatically
WIDTH=320
HEIGHT=240
FPS=5
DETECTION_MODEL=yolov5n
JPEG_QUALITY=60
```

### Pi 2 / Pi 3
```bash
# Optimized settings applied automatically
WIDTH=480
HEIGHT=360
FPS=8
DETECTION_MODEL=yolov5n
JPEG_QUALITY=65
```

### Pi 4 (4GB)
```bash
# Optimized settings applied automatically
WIDTH=640
HEIGHT=480
FPS=10
DETECTION_MODEL=yolov5n
JPEG_QUALITY=70
```

### Pi 4 (8GB) / Pi 5
```bash
# Higher performance settings
WIDTH=800
HEIGHT=600
FPS=12
DETECTION_MODEL=yolov5s  # Better accuracy
JPEG_QUALITY=75
```

---

## 🌐 Access Your Stream

Once running, access from any device on the same network:

### Direct URLs
- **📹 Main Stream:** `http://PI_IP_ADDRESS:8080/`
- **🎬 VLC Stream:** `http://PI_IP_ADDRESS:8080/stream`  
- **👥 Person API:** `http://PI_IP_ADDRESS:8080/api/persons`
- **❤️ Health Check:** `http://PI_IP_ADDRESS:8080/healthz`

### Find Your Pi IP
```bash
hostname -I    # Shows Pi IP address
# Example output: 192.168.1.150
```

### Access Examples
- From phone: `http://192.168.1.150:8080/`
- From laptop: `http://192.168.1.150:8080/`
- In VLC: Open Network Stream → `http://192.168.1.150:8080/stream`

---

## ⚙️ Configuration

### Custom Settings
```bash
# Copy example configuration
cp .env.example .env

# Edit settings
nano .env
```

### Key Settings for Pi
```bash
# Camera
CAMERA_INDEX=0          # 0 for Pi camera, 1+ for USB
WIDTH=640              # Lower for better performance
HEIGHT=480             # Lower for better performance
FPS=10                 # Lower for smoother stream

# Detection  
DETECTION_ENABLED=true
DETECTION_MODEL=yolov5n    # Fastest model for Pi
CONFIDENCE_THRESHOLD=0.5   # Person detection sensitivity

# Performance
JPEG_QUALITY=70        # Balance quality/performance
```

---

## 🎥 Camera Setup

### Pi Camera Module
```bash
# Test Pi camera
libcamera-hello --timeout 2000

# Check if detected
ls /dev/video*
# Should show: /dev/video0
```

### USB Webcam
```bash
# List available cameras
v4l2-ctl --list-devices

# Test USB camera
ffplay /dev/video1  # Usually video1 for USB
```

### Camera Troubleshooting
```bash
# Enable legacy camera support (if needed)
sudo raspi-config
# Advanced Options → GL Driver → G1 Legacy

# Check camera status
vcgencmd get_camera
# Should show: supported=1 detected=1
```

---

## 🚀 Running the Application

### Method 1: Complete Setup + Run
```bash
./setup-pi.sh          # Sets up everything and asks to start
```

### Method 2: Run After Setup
```bash
./run.sh               # Quick start (if already set up)
```

### Method 3: Manual Start
```bash
source .venv/bin/activate
python3 app.py
```

### Method 4: Background Service
```bash
# Run in background
nohup ./run.sh > stream.log 2>&1 &

# Check if running
ps aux | grep python
```

---

## 📊 Performance Tips

### Improve Performance
```bash
# 1. Lower resolution in .env
WIDTH=480
HEIGHT=360

# 2. Reduce FPS
FPS=8

# 3. Use fastest model
DETECTION_MODEL=yolov5n

# 4. Lower quality
JPEG_QUALITY=60

# 5. Disable detection for streaming only
DETECTION_ENABLED=false
```

### Monitor Performance
```bash
# Check CPU/RAM usage
htop

# Check temperature
vcgencmd measure_temp

# Check stream stats
curl http://localhost:8080/api/stats
```

### Cool Your Pi
- Use heatsinks for sustained performance
- Ensure good ventilation
- Consider a fan for Pi 4 under load

---

## 🔧 Troubleshooting

### Camera Issues
```bash
# Camera not detected
sudo raspi-config  # Enable camera interface
sudo reboot

# Permission denied
sudo usermod -a -G video pi
sudo reboot

# Check camera devices
ls -l /dev/video*
v4l2-ctl --list-devices
```

### Performance Issues
```bash
# Stream too slow
# → Lower WIDTH/HEIGHT in .env
# → Reduce FPS
# → Use yolov5n model

# High CPU usage
# → Disable detection: DETECTION_ENABLED=false
# → Lower resolution
# → Add cooling

# Memory issues (Pi Zero/1)
# → Use minimal requirements: pip install -r requirements-minimal.txt
# → Disable detection
```

### Network Issues
```bash
# Can't access from other devices
sudo ufw allow 8080/tcp     # Open firewall port
ip route show               # Check network

# Stream not loading
ping PI_IP_ADDRESS          # Test connectivity
curl http://localhost:8080/healthz  # Test locally
```

### Dependencies Issues
```bash
# PyTorch installation failed
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# OpenCV issues
sudo apt install -y python3-opencv
pip install opencv-python-headless

# Out of space
sudo apt clean
sudo apt autoremove
df -h  # Check disk space
```

---

## 🏃‍♂️ Running at Boot (Optional)

### Create systemd service
```bash
sudo nano /etc/systemd/system/person-detection.service
```

```ini
[Unit]
Description=Person Detection Stream
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/webcam-object-detection-stream
ExecStart=/home/pi/webcam-object-detection-stream/run.sh
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Enable and start
```bash
sudo systemctl daemon-reload
sudo systemctl enable person-detection.service
sudo systemctl start person-detection.service

# Check status
sudo systemctl status person-detection.service
```

---

## 📱 Use Cases

### Security Monitoring
- **Door/Entry monitoring** - Detect when people enter
- **Property surveillance** - Monitor outdoor areas
- **Package delivery** - Alert when delivery person arrives

### Home Automation
- **Occupancy detection** - Trigger lights when person detected
- **Smart doorbell** - Stream + person detection
- **Pet monitoring** - (detects people visiting pets)

### IoT Integration
- **MQTT publishing** - Send person detection events
- **Home Assistant** - Integrate with smart home
- **Webhook alerts** - Notify other systems

---

## 🔌 API Usage

### Get Person Detections
```bash
curl http://PI_IP:8080/api/persons
```

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
  "timestamp": 1674123456.789
}
```

### Health Check
```bash
curl http://PI_IP:8080/healthz
```

### Stream Stats
```bash
curl http://PI_IP:8080/api/stats
```

---

## 🔧 Advanced Configuration

### Custom Detection Area
```python
# Add to app.py for custom detection zones
def is_in_detection_zone(bbox, zone):
    # Define custom detection areas
    x1, y1, x2, y2 = bbox
    return (zone['x1'] <= x1 <= zone['x2'] and 
            zone['y1'] <= y1 <= zone['y2'])
```

### Webhook Notifications
```bash
# Add webhook URL to .env
WEBHOOK_URL=http://your-server.com/webhook

# Sends POST when person detected
```

### Multiple Camera Support
```bash
# Run multiple instances
CAMERA_INDEX=0 PORT=8080 python3 app.py &  # Pi camera
CAMERA_INDEX=1 PORT=8081 python3 app.py &  # USB camera
```

---

## 📝 Files Overview

**Included in ZIP file:**

```
webcam-object-detection-stream/
├── setup-pi.sh              # Complete Pi setup script
├── run.sh                    # Quick start script (Linux/Pi)
├── run.ps1                  # Windows PowerShell script
├── quick-start.sh           # Fast testing (no AI)
├── app.py                   # Main Python application
├── requirements.txt         # Full dependencies
├── requirements-pi.txt      # Pi-optimized packages
├── requirements-minimal.txt # Minimal dependencies
├── .env.example            # Configuration template
├── README.md               # Main documentation
├── README-PI.md            # This Pi-specific guide
├── LICENSE                 # MIT License
├── .gitignore              # Git ignore rules
├── templates/              # Web templates (not used)
├── static/                 # CSS files (not used)
└── models/                 # YOLO models (downloaded automatically)
```

**Key files for Pi users:**
- 🍓 **`setup-pi.sh`** - Complete Pi setup in one command
- 🏃 **`run.sh`** - Quick launch after setup
- ⚙️ **`requirements-pi.txt`** - Pi-optimized dependencies (CPU-only PyTorch)
- 📝 **`README-PI.md`** - This complete Pi guide

---

## 🆘 Getting Help

### Check Logs
```bash
# Application logs
tail -f stream.log

# System logs  
journalctl -u person-detection.service -f

# Pi system logs
dmesg | tail
```

### Common Commands
```bash
# Restart application
sudo systemctl restart person-detection.service

# Check Pi temperature
vcgencmd measure_temp

# Check available space
df -h

# Update system
sudo apt update && sudo apt upgrade
```

### Resources
- **Pi Camera Troubleshooting:** [raspberrypi.org/documentation](https://www.raspberrypi.org/documentation/usage/camera/)
- **Pi Performance:** Monitor with `htop` and `vcgencmd measure_temp`
- **Network Issues:** Check with `ping` and `ip route`

---

## 🎯 Summary

📦 **This ZIP distribution contains everything you need** - no git, no external downloads!

This system is **specifically optimized for Raspberry Pi** with:

- ✅ **Person detection only** (faster than 80+ objects)
- ✅ **CPU-only PyTorch** (no GPU needed)
- ✅ **Automatic Pi model detection** and optimization
- ✅ **Minimal resource usage**
- ✅ **Direct streaming** at root URL
- ✅ **One-command setup:** `./setup-pi.sh`
- ✅ **Standalone ZIP** - works offline after setup

**Perfect for:** Security cameras, smart doorbells, occupancy detection, IoT projects, and home automation.

---

## 🚀 Getting Started (TL;DR)

1. **Extract ZIP** on your Raspberry Pi
2. **Run:** `cd webcam-object-detection-stream && ./setup-pi.sh`
3. **Access:** `http://your-pi-ip:8080/` from any device
4. **Done!** 🎉

---

**🔗 Stream URL:** `http://your-pi-ip:8080/` - Works in any browser or VLC!

**📱 Mobile friendly** - Access from phones, tablets, laptops on same network

**🎯 Person detection** - Only detects people, optimized for Pi performance
