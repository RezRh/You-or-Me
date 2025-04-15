# Deployment Guide for You or Me? Game

## Prerequisites

1. Python 3.7 or higher
2. pip (Python package installer)
3. Required Python packages (install using pip):
   ```bash
   pip install requests speech_recognition gTTS playsound
   ```
4. OpenRouter API key from https://openrouter.ai/

## Running the Game

1. Clone or download the game files
2. Navigate to the game directory
3. Run the game:
   ```bash
   python main.py
   ```

## First-time Setup

1. When you first run the game, you'll be prompted to enter your OpenRouter API key
2. The API key will be saved for future use
3. Make sure your microphone and speakers are working properly

## Troubleshooting

- If you encounter issues with PyAudio installation:
  - macOS: `brew install portaudio`
  - Linux: `sudo apt-get install portaudio19-dev`
  - Windows: Install PyAudio wheel manually

- If speech recognition isn't working:
  - Check microphone permissions
  - Ensure microphone is properly connected
  - Try speaking clearly and at a normal volume

## Game Files

- `main.py`: Main game script
- `config.json`: Stores your API key
- `favorites.json`: Stores your favorite questions

Enjoy playing You or Me? Game!