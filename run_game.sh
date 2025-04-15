#!/bin/bash

# Run Game Script for You or Me? Game

echo "=== You or Me? Game Launcher ==="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

# Check if setup has been run
if [ ! -f "requirements.txt" ] || [ ! -f "config.json" ] || [ ! -f "favorites.json" ]; then
    echo "It seems this is your first time running the game."
    echo "Running setup first..."
    echo ""
    python3 setup.py
else
    # Run the game
    echo "Starting You or Me? Game..."
    echo ""
    python3 main.py
fi