# Sample Chord Mappings for Twiddler

This directory contains sample chord mapping configurations for different use cases.

## Files

- `default.conf` - Default chord mappings (QWERTY-like layout)
- `programmer.conf` - Optimized for programming with easy access to symbols
- `gaming.conf` - Gaming-focused layout with quick access to common game keys

## Usage

To use a sample configuration:

1. Copy the desired config file to the main config directory:
   ```bash
   copy config\samples\programmer.conf config\twiddler.conf
   ```

2. Edit `config/twiddler.conf` and adjust the `[Connection]` section for your COM port

3. Restart the Twiddler driver

## Creating Custom Mappings

Edit the `[ChordMap]` section to customize your layout:

```ini
[ChordMap]
# Single buttons
Button1=a
Button2=b
Button3=c
Button4=d

# Two-button chords
Button1+Button2=e
Button1+Button3=f

# Three-button chords
Button1+Button2+Button3=Space

# With modifiers
Button1+Shift=A
Button1+Button2+Ctrl=Ctrl+C
```

## Tips

- Start with a simple layout and gradually add complexity
- Group related keys together for easier learning
- Use the test utility to verify your mappings work correctly
- Keep a backup of your favorite configuration

## Contributing

Have a great chord mapping? Consider sharing it by:
1. Creating a new `.conf` file in this directory
2. Document the layout purpose and design
3. Submit a pull request
