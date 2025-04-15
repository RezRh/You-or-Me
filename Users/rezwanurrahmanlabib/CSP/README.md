# You or Me? Game

A fun interactive game that uses OpenRouter API to generate unlimited "You or Me?" questions with voice chat features (text-to-speech and speech-to-text).

## Features

- Unlimited "You or Me?" questions generated via OpenRouter API
- Voice interaction with text-to-speech and speech-to-text capabilities
- Scoring system to track "You" vs "Me" points
- Save your favorite questions for later
- Simple and intuitive interface

## Requirements

- Python 3.7 or higher
- OpenRouter API key (get one at https://openrouter.ai/)
- Microphone for speech input
- Speakers for voice output

## Installation

1. Clone or download this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

4. When prompted, enter your OpenRouter API key

## How to Play

1. The game will ask you a "You or Me?" question through both text and voice
2. Respond by saying either "You" or "Me" into your microphone
3. The game will track your score and give you the option to save favorite questions
4. Navigate through the menu to play rounds, view scores, and manage favorites

## Troubleshooting

- If you encounter issues with PyAudio installation, you may need to install portaudio first:
  - On macOS: `brew install portaudio`
  - On Linux: `sudo apt-get install portaudio19-dev`
  - On Windows: PyAudio wheel installation may be required

- If speech recognition isn't working, check that your microphone is properly connected and has system permissions

## License

MIT