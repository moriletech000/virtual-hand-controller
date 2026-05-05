#!/bin/bash

echo "Starting Virtual Mouse and Keyboard..."
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Running application..."
python main.py
