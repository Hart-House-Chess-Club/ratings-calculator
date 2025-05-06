#!/bin/bash
# filepath: start.sh

# Exit on error
set -e

# Step 1: Set up Python virtual environment if not present
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

# Step 2: Activate the virtual environment
source .venv/bin/activate

# Step 3: Install backend dependencies
pip install -r requirements.txt

# Step 4: Start Flask backend in background
echo "Starting Flask backend..."
FLASK_APP=app.py flask run > flask.log 2>&1 &

# Save backend PID to kill later if needed
BACKEND_PID=$!

# Step 5: Start frontend server
echo "Starting frontend server at http://localhost:8000 ..."
cd frontend
python3 -m http.server 8000 > ../frontend.log 2>&1 &

FRONTEND_PID=$!

# Step 6: Open frontend in default browser (Mac-specific)
open http://localhost:8000

echo "Both backend and frontend are running."
echo "To stop: kill $BACKEND_PID $FRONTEND_PID"