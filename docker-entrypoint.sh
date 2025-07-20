#!/bin/bash
set -e
echo "🌐 Launching ENGINE-AJ GUI with Xvfb..."

# Start virtual display
Xvfb :99 -screen 0 1280x880x24 &
export DISPLAY=:99

# Launch your PySide6 app
exec python3 engine_aj_web_3.0_demo.py
