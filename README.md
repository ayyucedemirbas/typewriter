# Typewriter Sounds

A macOS app that plays authentic typewriter sounds on every keypress.

## Features

- 🎵 Realistic typewriter sound generation
- 🔄 Toggle sounds on/off via menu bar
- ⚡ Low latency audio playback
- 🖥️ Native macOS integration
- 🔊 Programmatically generated sounds (no audio files needed)

## Usage

Run from terminal:

```bash
typewriter.py
```

The app will appear in your menu bar with a keyboard icon (⌨️). Click to toggle sounds on/off.

## Requirements

- macOS 10.14 or later
- Python 3.7+
- Accessibility permissions (required for keyboard monitoring)

## Permissions Setup

1. Open System Preferences → Security & Privacy → Privacy
2. Select "Accessibility" from the left sidebar
3. Click the lock to make changes
4. Add Terminal (or your Python IDE) to the list
5. Restart the application

## Development

Clone the repository:

```bash
git clone https://github.com/ayyucedemirbas/typewriter.git
cd typewriter-sounds
pip install -e .
```

## Dependencies

- numpy: Sound wave generation
- pygame: Audio playback
- pynput: Keyboard monitoring
- rumps: macOS menu bar integration

## License

General Public License v3.0 - see LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
