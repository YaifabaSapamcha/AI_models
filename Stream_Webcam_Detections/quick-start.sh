#!/bin/bash
# Quick Start - Minimal setup for immediate testing
# This installs minimal dependencies and starts streaming (no AI detection)

echo "⚡ Quick Start - Person Detection Stream"
echo "========================================"
echo "🚀 This will start basic camera streaming (detection disabled for speed)"
echo ""

# Create venv if needed
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install minimal requirements
echo "📚 Installing minimal dependencies (fast)..."
pip install --upgrade pip
pip install -r requirements-minimal.txt

# Create basic config
if [ ! -f ".env" ]; then
    echo "⚙️ Creating basic configuration..."
    cat > .env << EOF
HOST=0.0.0.0
PORT=8080
CAMERA_INDEX=0
WIDTH=640
HEIGHT=480
FPS=15
DETECTION_ENABLED=false
EOF
fi

# Show access info
PI_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "localhost")
echo ""
echo "🌟 Starting basic camera stream..."
echo "📹 Access: http://$PI_IP:8080/"
echo "🎬 VLC: http://$PI_IP:8080/stream"
echo ""
echo "⚠️  Person detection is DISABLED for this quick start"
echo "💡 For full features, run: ./run.sh"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start with detection disabled
DETECTION_ENABLED=false python3 app.py