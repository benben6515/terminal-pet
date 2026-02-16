# Nyan Cat Terminal Pet 🐱✨

An interactive Nyan cat terminal pet with rainbow colors, animations, and pet care mechanics!

## Features

- **Animated Nyan Cat** with smooth frame animations
- **Rainbow tail** with smooth color fading effect (256-color ANSI)
- **Interactive controls** - feed, play, pet, and sleep with your cat
- **Stats system** - manage hunger, mood, and energy
- **Random behaviors** - cat performs spontaneous actions
- **Twinkling star background**
- **Configurable** settings via YAML

## Installation

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
python test.py
```

4. Run the pet:
```bash
python main.py
```

**Quick Start:**
```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `f` | Feed the cat |
| `p` | Play with the cat |
| `t` | Pet the cat |
| `s` | Put cat to sleep |
| `h` | Toggle help menu |
| `q` | Quit |

## Stats

- **Hunger**: Decreases over time, feed to restore
- **Mood**: Affected by interactions and hunger
- **Energy**: Depletes with play, restores with sleep

## Configuration

Edit `config.yaml` to customize:
- Animation speed
- Movement speed
- Stats decay rates
- Colors
- Controls

## Requirements

- Python 3.8+
- Terminal with 256-color support
- Works on Linux, macOS, and Windows (with modern terminal)

## License

MIT License - Feel free to customize and have fun! 🌈
# terminal-pet
