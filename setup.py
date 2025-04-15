#!/usr/bin/env python3

import os
import sys
import subprocess
import json

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        print(f"Current Python version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required packages"""
    print("\n=== Installing Dependencies ===")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_config_file():
    """Create config.json file if it doesn't exist"""
    if not os.path.exists("config.json"):
        try:
            with open("config.json", "w") as f:
                json.dump({"api_key": ""}, f)
            print("Created config.json file")
        except Exception as e:
            print(f"Error creating config.json: {e}")

def create_favorites_file():
    """Create favorites.json file if it doesn't exist"""
    if not os.path.exists("favorites.json"):
        try:
            with open("favorites.json", "w") as f:
                json.dump([], f)
            print("Created favorites.json file")
        except Exception as e:
            print(f"Error creating favorites.json: {e}")

def main():
    print("=== You or Me? Game Setup ===")
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create necessary files
    create_config_file()
    create_favorites_file()
    
    print("\n=== Setup Complete! ===")
    print("To run the game, use: python main.py")
    print("\nNote: You will need an OpenRouter API key from https://openrouter.ai/")
    
    # Ask if user wants to run the game now
    run_now = input("\nDo you want to run the game now? (y/n): ").lower()
    if run_now == 'y':
        print("\nStarting the game...\n")
        try:
            subprocess.call([sys.executable, "main.py"])
        except Exception as e:
            print(f"Error starting the game: {e}")

if __name__ == "__main__":
    main()