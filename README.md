# You or Me? Game

A fun voice-based game where you answer questions about who is more likely to do something - you or someone else!

## Features

- Voice-based interaction using speech recognition
- Text-to-speech for game prompts and feedback
- AI-generated "You or Me?" questions using OpenRouter API
- Save favorite questions for future games
- Track and reset scores

## Requirements

- Python 3.7 or higher
- OpenRouter API key (get one at https://openrouter.ai/)
- Microphone for speech input
- Speakers for voice output

## Installation

1. Clone or download this repository
2. Run the setup script to install dependencies:

```bash
python setup.py
```

This will:
- Install required Python packages
- Create necessary configuration files
- Offer to start the game immediately

## Manual Installation

If you prefer to install manually:

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python main.py
```

## First Run

On first run, you'll be prompted to enter your OpenRouter API key. You can get one for free at https://openrouter.ai/.

## How to Play

1. The game will ask "You or Me?" questions
2. Answer verbally with either "You" or "Me"
3. The game keeps score of your answers
4. You can save favorite questions for future games

## Troubleshooting

- **Microphone issues**: Ensure your microphone is properly connected and has permission to be accessed
- **API errors**: Verify your OpenRouter API key is correct
- **Audio playback issues**: Check your speaker/headphone connection and volume settings

## License

This project is open source and available under the MIT License.