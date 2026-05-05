#!/usr/bin/env bash
# DjangoVibe demo launcher (macOS/Linux)
set -e

if [ ! -d "venv" ]; then
    echo "[!] venv not found. Run setup first:"
    echo "    python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo "Launching Streamlit #1 on :8501 (logs -> /tmp/streamlit1.log)"
streamlit run streamlit_apps/dashboard1.py --server.port 8501 > /tmp/streamlit1.log 2>&1 &
PID1=$!

echo "Launching Streamlit #2 on :8502 (logs -> /tmp/streamlit2.log)"
streamlit run streamlit_apps/dashboard2.py --server.port 8502 > /tmp/streamlit2.log 2>&1 &
PID2=$!

trap "kill $PID1 $PID2 2>/dev/null" EXIT

echo "Launching Django on :8000 (Ctrl+C to stop everything)"
python manage.py runserver
