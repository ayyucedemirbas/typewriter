# Typewriter Sounds

A macOS app that plays authentic typewriter sounds on every keypress with multiple typewriter models and customizable settings.

## Features

- 🎵 **Multiple Typewriter Models**: Classic Typewriter, IBM Selectric, Mechanical Keyboard
- 🔊 **Advanced Key Detection**: Unique sounds for 11 different key types
- 🎚️ **Volume Control**: 4 volume levels (25%, 50%, 75%, 100%)
- 🎲 **Realistic Sound Variation**: Complex physics-based sound synthesis
- 🔄 **Easy Toggle**: Turn sounds on/off via menu bar
- ⚡ **Low Latency**: Optimized audio playbook
- 🖥️ **Native macOS Integration**: Clean menu bar interface
- 🔊 **No Audio Files**: Advanced programmatic sound generation
- 🎼 **Authentic Audio**: Multi-layered sound with reverb and velocity sensitivity

## Installation & Usage

### Quick Install (Recommended)
```bash
# Clone the repository
git clone https://github.com/mehmetkahya0/typewriter.git
cd typewriter

# Run the install script
./install.sh

# Start the app
python3 typewriter.py
```

### Manual Installation
1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the app**:
```bash
python typewriter.py
```

3. **Menu Options**:
   - Click the keyboard icon (⌨️) in your menu bar
   - **Toggle Sounds**: Enable/disable typewriter sounds
   - **Typewriter Model**: Choose between Classic, IBM Selectric, or Mechanical Keyboard
   - **Volume**: Adjust sound level (25%, 50%, 75%, 100%)

## Typewriter Models

- **Classic Typewriter**: Deep, mechanical sounds with rich low frequencies
- **IBM Selectric**: Precise, electronic sounds with balanced frequencies  
- **Mechanical Keyboard**: Sharp, clicky sounds with emphasis on high frequencies

## Special Key Sounds

### Enhanced Key Detection (11 Key Types):
- **Regular Letters**: Natural typing variations with velocity sensitivity
- **Numbers**: Slightly higher pitch with precision feel
- **Punctuation**: Sharp, precise sounds for accuracy
- **Symbols**: Distinctive higher-pitched sounds
- **Space Bar**: Deep, resonant sound with longer duration
- **Enter Key**: Includes authentic typewriter "bell" sound
- **Backspace**: Quick, higher-pitched correction sound
- **Tab Key**: Moderate depth with mechanical precision
- **Modifier Keys** (Shift, Ctrl, Alt, Cmd): Deeper, sustained sounds
- **Arrow Keys**: Light, precise navigation sounds
- **Special Keys**: Balanced sounds for function keys

### Advanced Audio Features:
- **Physics-Based Synthesis**: Realistic hammer, spring, and contact modeling
- **Multi-Layer Noise**: White noise, pink noise, and mechanical resonance
- **Velocity Sensitivity**: Typing force affects sound intensity
- **Micro-Variations**: Each keystroke is slightly unique
- **Subtle Reverb**: 8ms reverb for spatial authenticity
- **Soft Limiting**: Prevents clipping while maintaining dynamics

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

- **numpy**: Sound wave generation and mathematical operations
- **pygame**: Low-latency audio playback
- **pynput**: Cross-platform keyboard monitoring
- **rumps**: macOS menu bar integration

Install all dependencies:
```bash
pip install -r requirements.txt
```

## License

General Public License v3.0 - see LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
