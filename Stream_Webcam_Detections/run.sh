#!/usr/bin/env bash
set -euo pipefail

echo "👁️ Person Detection Stream Setup & Launch"
echo "==============================================="

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "🔄 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "🔍 Upgrading pip..."
pip install --upgrade pip

# Check if running on Raspberry Pi and use appropriate requirements
echo "📚 Installing dependencies..."
if [[ "$(uname -m)" == "arm"* ]] || [[ "$(uname -m)" == "aarch64" ]]; then
    if [ -f "requirements-pi.txt" ]; then
        echo "🍓 Detected Raspberry Pi - using optimized requirements..."
        pip install -r requirements-pi.txt
    else
        echo "⚠️ Pi detected but requirements-pi.txt not found, using standard requirements..."
        pip install -r requirements.txt
    fi
else
    echo "💻 Using standard requirements for desktop/laptop..."
    pip install -r requirements.txt
fi

echo "✅ All dependencies installed successfully!"

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo "⚙️ Loading environment variables from .env..."
    set -a
    source .env
    set +a
else
    echo "ℹ️ No .env file found. Using default settings."
    echo "💡 Copy .env.example to .env to customize settings."
fi

# Check for camera (Linux/Pi only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🎥 Checking camera availability..."
    if [ -e "/dev/video${CAMERA_INDEX:-0}" ]; then
        echo "✅ Camera found at /dev/video${CAMERA_INDEX:-0}"
    else
        echo "⚠️ Camera not found at /dev/video${CAMERA_INDEX:-0}"
        echo "   The application will still start, but may fail when accessing the camera."
    fi
fi

# Display configuration
echo ""
echo "📋 Configuration:"
echo "   Host: ${HOST:-0.0.0.0}"
echo "   Port: ${PORT:-8080}"
echo "   Camera: ${CAMERA_INDEX:-0}"
echo "   Resolution: ${WIDTH:-640}x${HEIGHT:-480}"
echo "   FPS: ${FPS:-10}"
echo "   Detection: ${DETECTION_ENABLED:-true}"
echo "   Model: ${DETECTION_MODEL:-yolov5n}"
echo ""

# Start the application
echo "👁️ Starting Person Detection Stream..."
echo "📹 Direct stream: http://${HOST:-0.0.0.0}:${PORT:-8080}/"
echo "🎬 VLC stream: http://${HOST:-0.0.0.0}:${PORT:-8080}/stream"
echo "👥 Person API: http://${HOST:-0.0.0.0}:${PORT:-8080}/api/persons"
echo "📊 Stats API: http://${HOST:-0.0.0.0}:${PORT:-8080}/api/stats"
echo "❤️ Health check: http://${HOST:-0.0.0.0}:${PORT:-8080}/healthz"
echo "📝 Info: http://${HOST:-0.0.0.0}:${PORT:-8080}/info"
echo ""
echo "🎯 Detection: PERSONS ONLY"
echo "🤖 Model: Optimized for performance"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Use waitress for production-like serving
python3 - <<'PY'
import os
from waitress import serve
from app import create_app

host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8080"))
app = create_app()

print(f"🌟 Person Detection Server starting on {host}:{port}")
print(f"🔗 Access: http://{host}:{port}/")
try:
    serve(app, host=host, port=port, threads=4)
except KeyboardInterrupt:
    print("\n🛑 Server stopped by user")
except Exception as e:
    print(f"\n❌ Server error: {e}")
PY
