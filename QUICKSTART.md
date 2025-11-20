# Twiddler Quick Reference

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Find Your COM Port
- Open Device Manager (Win + X → Device Manager)
- Expand "Ports (COM & LPT)"
- Note the COM port number (e.g., COM3)

### 3. Configure
Edit `config/twiddler.conf`:
```ini
[Connection]
COMPort=COM3  # Change to your port
```

### 4. Run
```bash
python src/twiddler_driver.py
```
Or double-click `start_twiddler.bat`

## Common Commands

### Test Connection
```bash
python tools/test_connection.py COM3
```

### List Available Ports
```bash
python tools/test_connection.py --list
```

### Enable Debug Mode
Edit `config/twiddler.conf`:
```ini
[Advanced]
DebugMode=True
```

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "Failed to connect" | Check COM port in Device Manager |
| No keyboard input | Enable debug mode, check logs |
| Permission errors | Run as Administrator |
| High CPU usage | Increase sleep time in config |
| Mouse too fast/slow | Adjust `Sensitivity` in config |

## Configuration Shortcuts

### Change Baud Rate
```ini
[Connection]
BaudRate=19200  # Try 4800, 9600, or 19200
```

### Adjust Mouse Sensitivity
```ini
[Mouse]
Sensitivity=1.5  # 0.1 to 2.0, default is 1.0
```

### Custom Chord Mapping
```ini
[ChordMap]
Button1+Button2=your_key
```

## File Locations

| File | Purpose |
|------|---------|
| `config/twiddler.conf` | Main configuration |
| `twiddler.log` | Log file (when debug enabled) |
| `src/twiddler_driver.py` | Driver program |
| `INSTALL.md` | Full installation guide |
| `HARDWARE.md` | Hardware setup guide |
| `BLUETOOTH.md` | Bluetooth guide |

## Hardware Connection

### USB Setup
1. Connect USB-to-Serial adapter to PC
2. Connect Twiddler to adapter (9-pin serial)
3. Connect PS/2 power if needed
4. Note COM port number
5. Update config file

### Bluetooth Setup
See [BLUETOOTH.md](BLUETOOTH.md) for complete guide.

## Getting Help

1. Check [INSTALL.md](INSTALL.md) for detailed instructions
2. Enable debug mode and check logs
3. Test connection with `tools/test_connection.py`
4. Verify hardware connections
5. Check Device Manager for COM port issues

## Useful Links

- [Georgia Tech Bluetooth Twiddler](https://wiki.cc.gatech.edu/ccg/classes/7470/7470-f06/bluetooth_twiddler)
- [HandyKey Official](http://www.handykey.com/)
- [DIY Wireless Keyboards](http://www.reddit.com/r/MechanicalKeyboards/wiki/wireless-mechanical_keyboards)
