#!/bin/bash
# Raspberry Pi Person Detection Stream Setup
set -e

echo "🍓 Raspberry Pi Person Detection Stream Setup"
echo "=============================================="

# Detect Pi model
PI_MODEL=$(cat /proc/device-tree/model 2>/dev/null | tr -d '\0' || echo "Unknown")
echo "📟 Detected: $PI_MODEL"

# Update system
echo "📦 Updating system packages..."
sudo apt update

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    libopencv-dev \
    python3-opencv \
    v4l-utils \
    git

# Check camera
echo "🎥 Checking camera..."
if [ -e "/dev/video0" ]; then
    echo "✅ Camera detected at /dev/video0"
    v4l2-ctl --list-devices || echo "⚠️ v4l2-ctl not available"
else
    echo "❌ No camera detected at /dev/video0"
    echo "💡 Make sure camera is connected and enabled:"
    echo "   sudo raspi-config -> Interface Options -> Camera -> Enable"
fi

# Create Python virtual environment
echo "🐍 Setting up Python environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies with optimizations for Pi
echo "📚 Installing Python packages (this may take a while on Pi)..."
echo "🔥 Using CPU-only PyTorch for optimal Pi performance..."

# Use Pi-optimized requirements file
if [ -f "requirements-pi.txt" ]; then
    echo "📦 Installing from requirements-pi.txt (Pi optimized)..."
    pip install -r requirements-pi.txt
else
    echo "📦 Installing individual packages..."
    # Fallback to individual installs
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    pip install Flask opencv-python-headless numpy waitress ultralytics PyYAML requests pandas psutil
fi

# Create optimized configuration for Pi
echo "⚙️ Creating Pi-optimized configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    
    # Detect Pi model and set optimal settings
    if [[ "$PI_MODEL" =~ "Pi Zero" ]] || [[ "$PI_MODEL" =~ "Pi 1" ]]; then
        echo "🔧 Optimizing for Pi Zero/1..."
        sed -i 's/WIDTH=640/WIDTH=320/' .env
        sed -i 's/HEIGHT=480/HEIGHT=240/' .env  
        sed -i 's/FPS=10/FPS=5/' .env
        sed -i 's/yolov5n/yolov5n/' .env
    elif [[ "$PI_MODEL" =~ "Pi 2" ]] || [[ "$PI_MODEL" =~ "Pi 3" ]]; then
        echo "🔧 Optimizing for Pi 2/3..."
        sed -i 's/WIDTH=640/WIDTH=480/' .env
        sed -i 's/HEIGHT=480/HEIGHT=360/' .env
        sed -i 's/FPS=10/FPS=8/' .env
        sed -i 's/yolov5n/yolov5n/' .env
    elif [[ "$PI_MODEL" =~ "Pi 4" ]]; then
        echo "🔧 Optimizing for Pi 4..."
        # Keep default settings (640x480, FPS=10, yolov5n)
        echo "Using default Pi 4 settings"
    fi
fi

# Test camera access
echo "📷 Testing camera access..."
python3 - <<'EOF'
import cv2
try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print("✅ Camera test successful!")
            print(f"   Frame size: {frame.shape[1]}x{frame.shape[0]}")
        else:
            print("❌ Failed to read from camera")
        cap.release()
    else:
        print("❌ Failed to open camera")
except Exception as e:
    print(f"❌ Camera test failed: {e}")
EOF

# Check free memory
echo "💾 System resources:"
free -h | grep -E 'Mem:|Swap:'

# Display final instructions
echo ""
echo "🎉 Setup complete!"
echo ""
echo "🎯 This system detects PERSONS ONLY"
echo "⚡ Optimized for Raspberry Pi performance"
echo ""
echo "🌐 Access the stream:"
echo "   Direct video: http://$(hostname -I | awk '{print $1}'):8080/"
echo "   Person API:   http://$(hostname -I | awk '{print $1}'):8080/api/persons"
echo "   Health check: http://$(hostname -I | awk '{print $1}'):8080/healthz"
echo ""
echo "📱 From other devices on the network:"
echo "   http://$(hostname -I | awk '{print $1}'):8080/"
echo ""
echo "💡 Performance tips:"
echo "   - Lower resolution in .env file if needed"
echo "   - Reduce FPS for slower Pi models"
echo "   - Use yolov5n model for fastest detection"
echo ""
echo "========================================"
echo "🚀 Starting Person Detection Stream..."
echo "========================================"
echo ""

# Ask user if they want to start immediately
read -p "Start the person detection stream now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌟 Launching person detection stream..."
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    # Load environment variables
    if [ -f ".env" ]; then
        set -a
        source .env
        set +a
    fi
    
    # Display final launch info
    PI_IP=$(hostname -I | awk '{print $1}')
    echo "👁️ Person Detection Stream Starting..."
    echo "📹 Direct stream: http://$PI_IP:${PORT:-8080}/"
    echo "🎬 VLC stream: http://$PI_IP:${PORT:-8080}/stream"
    echo "👥 Person API: http://$PI_IP:${PORT:-8080}/api/persons"
    echo ""
    
    # Start the application
    python3 - <<'PY'
import os
from waitress import serve
from app import create_app

host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8080"))
app = create_app()

print(f"🌟 Person Detection Server running on {host}:{port}")
try:
    serve(app, host=host, port=port, threads=4)
except KeyboardInterrupt:
    print("\n🛑 Server stopped by user")
except Exception as e:
    print(f"\n❌ Server error: {e}")
PY
else
    echo ""
    echo "🚀 To start later, run: ./run.sh"
    echo "📝 Or: python3 app.py"
fi
