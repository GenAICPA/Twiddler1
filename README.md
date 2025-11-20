# Twiddler1

Connect your 1990s era Twiddler handheld keyboard/mouse to modern Windows 11 computers via USB or Bluetooth.

## Overview

This project provides software and documentation to enable the original Twiddler handheld keyboard/mouse device to work with Windows 11. The Twiddler is a one-handed chording keyboard with integrated mouse functionality, originally designed with a 9-pin serial port output.

## Features

- **USB Support**: Connect via USB-to-Serial adapter
- **Bluetooth Support**: Wireless connection via Bluetooth serial modules
- **Full Keyboard Emulation**: All chord combinations supported
- **Mouse Integration**: Movement and button clicks
- **Configurable Mappings**: Customize key chords to your preference
- **Windows 11 Compatible**: Native HID input emulation

## Quick Start

1. **Install Python 3.7+** (if not already installed)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Connect hardware** (USB-to-Serial adapter + Twiddler)
4. **Configure COM port** in `config/twiddler.conf`
5. **Run the driver**:
   ```bash
   python src/twiddler_driver.py
   ```
   Or on Windows, double-click `start_twiddler.bat`

## Documentation

- **[Installation Guide](INSTALL.md)** - Complete setup instructions
- **[Hardware Setup](HARDWARE.md)** - Required adapters and connections
- **[Bluetooth Setup](BLUETOOTH.md)** - Wireless configuration guide
- **[Protocol Specification](docs/PROTOCOL.md)** - Technical details of Twiddler serial protocol

## Hardware Requirements

### Minimum
- Original Twiddler device with 9-pin serial port
- USB-to-Serial adapter (FTDI recommended)
- Windows 11 computer
- Python 3.7 or higher

### Optional (for Bluetooth)
- Bluetooth Serial Port Profile (SPP) module
- Basic soldering equipment
- See [BLUETOOTH.md](BLUETOOTH.md) for details

## System Requirements

- Windows 11 (64-bit)
- Python 3.7 or higher
- Administrator privileges (for keyboard/mouse emulation)
- Available USB port or Bluetooth capability

## Project Structure

```
Twiddler1/
├── README.md              # This file
├── INSTALL.md             # Installation guide
├── HARDWARE.md            # Hardware setup guide
├── BLUETOOTH.md           # Bluetooth configuration
├── requirements.txt       # Python dependencies
├── start_twiddler.bat     # Windows startup script
├── config/
│   └── twiddler.conf      # Configuration file
├── src/
│   └── twiddler_driver.py # Main driver program
├── docs/
│   └── PROTOCOL.md        # Protocol specification
└── tools/
    ├── README.md          # Tools documentation
    └── test_connection.py # Connection test utility
```

## Configuration

Edit `config/twiddler.conf` to customize:
- COM port and baud rate
- Mouse sensitivity
- Chord mappings
- Debug logging

## Testing

Test your connection before running the full driver:

```bash
python tools/test_connection.py COM3
```

This will display raw packets from the Twiddler to verify the connection.

## Troubleshooting

### Common Issues

1. **"Failed to connect to COM port"**
   - Verify COM port number in Device Manager
   - Check that adapter is properly connected
   - Ensure no other program is using the port

2. **No keyboard input**
   - Enable debug mode in config file
   - Check log file for errors
   - Verify Twiddler is powered on

3. **Permission errors**
   - Run as Administrator (required for keyboard/mouse emulation)

See [INSTALL.md](INSTALL.md) for detailed troubleshooting.

## Contributing

Contributions welcome! Areas for improvement:
- Additional chord mapping presets
- Support for other Twiddler models
- Linux/macOS support
- GUI configuration tool

## References

- [Georgia Tech Bluetooth Twiddler Project](https://wiki.cc.gatech.edu/ccg/classes/7470/7470-f06/bluetooth_twiddler)
- [HandyKey Official Site](http://www.handykey.com/)
- [DIY Wireless Keyboard Modifications](http://www.reddit.com/r/MechanicalKeyboards/wiki/wireless-mechanical_keyboards)

## License

This project is provided as-is for educational and personal use.

## Disclaimer

This is a community-developed driver not affiliated with HandyKey Corporation. The Twiddler serial protocol specification is based on reverse engineering and community documentation. Always consult official documentation when available.

---

**Note**: This driver is designed for the original Twiddler (Twiddler 1). For newer models (Twiddler 2/3), check the manufacturer's website for official Windows 11 drivers.
