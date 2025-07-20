#!/bin/bash
set -e

echo "🌐 Launching ENGINE-AJ GUI with Xvfb..."

# Start virtual framebuffer for GUI
Xvfb :99 -screen 0 1920x1080x24 &

# Export display for Qt to use
export DISPLAY=:99

# Start minimal window manager
fluxbox &

# Start VNC server (non-password mode)
x11vnc -forever -nopw -display :99 -rfbport 5900 &

# Launch noVNC WebSocket proxy
websockify --web=/usr/share/novnc 6080 localhost:5900 &

echo "🚀 Starting ENGINE-AJ Web App..."
exec python3 /app/engine_aj_web_3.0_demo.py
