# 🍓 Quick Install Guide for Raspberry Pi

**30-second setup checklist**

## ✅ Prerequisites
- [ ] Raspberry Pi with Raspberry Pi OS
- [ ] Camera connected (Pi Camera or USB)
- [ ] Internet connection (for setup only)
- [ ] ZIP file extracted on Pi

## 🚀 Installation Steps

### 1. Extract ZIP (if not done)
```bash
unzip webcam-detection-stream.zip
cd webcam-object-detection-stream
```

### 2. Enable Camera
```bash
sudo raspi-config
# Interface Options → Camera → Enable
sudo reboot
```

### 3. Run Setup
```bash
chmod +x setup-pi.sh
./setup-pi.sh
```

### 4. Access Stream
- **From browser:** `http://PI_IP:8080/`
- **From VLC:** `http://PI_IP:8080/stream`

### 5. Find Pi IP
```bash
hostname -I
```

## 🎯 That's it!

- ✅ **Person detection** running on your Pi
- ✅ **Stream accessible** from any device on network  
- ✅ **Optimized** for your Pi model automatically

---

**Need help?** See [README-PI.md](README-PI.md) for complete guide.

**Quick test?** Run `./quick-start.sh` for streaming without AI detection.