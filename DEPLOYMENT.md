# Deployment Guide for You or Me? Game

## Prerequisites

1. Python 3.7 or higher
2. pip (Python package installer)
3. Required Python packages (install using pip):
   ```bash
   pip install requests speech_recognition gTTS playsound
   ```
4. OpenRouter API key from https://openrouter.ai/

## Installation Options

### Option 1: Automated Setup (Recommended)

1. Run the setup script:
   ```bash
   python setup.py
   ```
   This will:
   - Check your Python version
   - Install all required dependencies
   - Create necessary configuration files
   - Offer to start the game immediately

### Option 2: Manual Installation

1. Install dependencies manually:
   ```bash
   pip install -r requirements.txt
   ```

2. Create required files:
   - Create an empty `config.json` file with: `{"api_key": ""}`
   - Create an empty `favorites.json` file with: `[]`

## Running the Game

```bash
python main.py
```

On first run, you'll be prompted to enter your OpenRouter API key.

## Deployment Options

### Local Deployment

The game runs locally on your machine and requires:
- Microphone access
- Speaker/audio output
- Internet connection (for API calls)

### Creating an Executable

You can create a standalone executable using PyInstaller:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create the executable:
   ```bash
   pyinstaller --onefile main.py
   ```

3. The executable will be created in the `dist` directory

### Distribution

To distribute the game to others:

1. Share the entire directory with all files
2. Instruct users to run `setup.py` first
3. Each user will need their own OpenRouter API key

## Troubleshooting

- **Speech recognition issues**: Ensure microphone is properly connected and has system permissions
- **API errors**: Verify API key is correct and has sufficient credits
- **Audio playback issues**: Check speaker connections and volume settings
- **Missing dependencies**: Run `pip install -r requirements.txt` to ensure all packages are installed