# 📦 Raspberry Pi Person Detection Stream - ZIP Distribution

**Ready-to-use ZIP package for Raspberry Pi users**

---

## 🎯 What's Included

This ZIP contains a **complete person detection streaming system** optimized for Raspberry Pi. No additional downloads required except Python packages during setup.

### 📋 Package Contents

| File | Purpose |
|------|---------|
| **🍓 setup-pi.sh** | Complete Pi setup script (one command install) |
| **🏃 run.sh** | Quick launch script for Linux/Pi |
| **💻 run.ps1** | Windows PowerShell script |
| **⚡ quick-start.sh** | Fast testing without AI detection |
| **🐍 app.py** | Main Python application |
| **📄 README-PI.md** | Complete Raspberry Pi guide |
| **📋 INSTALL-PI.md** | Quick installation checklist |
| **📖 README.md** | General documentation |
| **📦 requirements-pi.txt** | Pi-optimized dependencies (CPU-only PyTorch) |
| **📦 requirements.txt** | Full dependencies for desktop/laptop |
| **📦 requirements-minimal.txt** | Minimal dependencies for testing |
| **⚙️ .env.example** | Configuration template |
| **📜 LICENSE** | MIT License |

---

## 🚀 Quick Start for Pi Users

**30-second setup:**

```bash
# 1. Extract ZIP on your Raspberry Pi
unzip raspberry-pi-person-detection-stream.zip
cd webcam-object-detection-stream

# 2. Run setup script
chmod +x setup-pi.sh
./setup-pi.sh

# 3. Access from any device on your network
# Browser: http://your-pi-ip:8080/
# VLC: http://your-pi-ip:8080/stream
```

---

## 🎛️ Features

- 👥 **Person Detection Only** - Optimized for Pi performance
- 🍓 **Pi Model Auto-Detection** - Optimizes settings for Pi Zero to Pi 5
- 📹 **Direct Video Streaming** - No web interface, just pure video at root URL
- 📱 **Network Access** - View from phones, tablets, laptops on same Wi-Fi
- 🎬 **VLC Compatible** - Works with VLC media player
- 📡 **REST API** - Get person detection data as JSON
- ⚙️ **Configurable** - Adjust resolution, FPS, model size

---

## 🎯 Optimized Performance

### Pi Model Auto-Optimization:
- **Pi Zero/1:** 320x240, 5fps, yolov5n
- **Pi 2/3:** 480x360, 8fps, yolov5n
- **Pi 4 (4GB):** 640x480, 10fps, yolov5n
- **Pi 4 (8GB)/Pi 5:** 800x600, 12fps, yolov5s

### CPU-Only PyTorch:
- ✅ **80% smaller** download vs GPU version
- ✅ **Faster installation** on Pi
- ✅ **Lower memory usage**
- ✅ **Better compatibility** with all Pi models

---

## 📱 Access Methods

Once running, access from any device on the same network:

### Direct URLs:
- **📹 Main Stream:** `http://PI_IP:8080/`
- **🎬 VLC Stream:** `http://PI_IP:8080/stream`
- **👥 Person API:** `http://PI_IP:8080/api/persons`
- **❤️ Health Check:** `http://PI_IP:8080/healthz`

### Example Usage:
```bash
# Find your Pi IP
hostname -I

# Example: 192.168.1.150
# Access from phone: http://192.168.1.150:8080/
# Access from laptop: http://192.168.1.150:8080/
# VLC stream: http://192.168.1.150:8080/stream
```

---

## 🔧 Requirements

### Hardware:
- Raspberry Pi (any model - Zero, 3, 4, 5)
- Camera (Pi Camera Module or USB webcam)
- 8GB+ SD Card (16GB+ recommended)
- Stable power supply

### Software:
- Raspberry Pi OS (Bookworm/Bullseye)
- Python 3.8+ (pre-installed)
- Internet connection (for initial setup only)

---

## 💡 Use Cases

- **🏠 Security Monitoring** - Door/entry detection
- **🔔 Smart Doorbell** - Person detection + streaming
- **🏡 Home Automation** - Occupancy detection
- **🎓 Educational Projects** - Learn computer vision
- **🔧 IoT Integration** - Person detection for smart home

---

## 📚 Documentation

- **📖 Complete Guide:** [README-PI.md](README-PI.md)
- **⚡ Quick Install:** [INSTALL-PI.md](INSTALL-PI.md)
- **💻 General Info:** [README.md](README.md)

---

## 🆘 Support

### Common Issues:
- **Camera not detected:** Enable camera in `raspi-config`
- **Slow performance:** Use smaller resolution/model
- **Network issues:** Check firewall, use Pi IP address
- **Installation fails:** Check internet connection, try `requirements-minimal.txt` first

### Performance Tips:
- Lower resolution for better FPS
- Use `yolov5n` model for fastest detection  
- Add heatsinks/cooling for sustained performance
- Monitor temperature with `vcgencmd measure_temp`

---

## 📄 License

MIT License - Free for personal and commercial use

---

**🎉 Ready to stream? Extract the ZIP and run `./setup-pi.sh`!**