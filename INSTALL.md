# Installation Guide for Twiddler on Windows 11

## Overview
This guide walks you through the complete installation process for using your original Twiddler handheld keyboard/mouse with Windows 11.

## Prerequisites

### Hardware
1. Original Twiddler device with 9-pin serial port
2. USB to Serial adapter (FTDI recommended) OR Bluetooth serial module
3. PS/2 power adapter (if required by your Twiddler model)
4. Windows 11 computer

### Software
1. Windows 11 (64-bit recommended)
2. Python 3.7 or higher
3. Administrator access for driver installation

## Installation Steps

### Step 1: Install Python

1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   ```

### Step 2: Install Serial Adapter Drivers

#### For USB to Serial Adapter:
1. Connect your USB to Serial adapter to the computer
2. Windows 11 should automatically install drivers
3. If drivers don't install automatically:
   - Visit the manufacturer's website (e.g., FTDI, Prolific)
   - Download and install the appropriate drivers
4. Verify installation:
   - Open Device Manager (Win + X → Device Manager)
   - Expand "Ports (COM & LPT)"
   - Note the COM port number (e.g., COM3)

#### For Bluetooth Adapter:
See [BLUETOOTH.md](BLUETOOTH.md) for detailed Bluetooth setup instructions.

### Step 3: Download Twiddler Driver

1. Clone or download this repository:
   ```cmd
   git clone https://github.com/GenAICPA/Twiddler1.git
   cd Twiddler1
   ```

2. Or download as ZIP and extract to a folder

### Step 4: Install Python Dependencies

Open Command Prompt as Administrator and run:

```cmd
cd Twiddler1
pip install pyserial keyboard mouse
```

If you encounter permission errors:
```cmd
pip install --user pyserial keyboard mouse
```

### Step 5: Configure the Driver

1. Open `config/twiddler.conf` in a text editor
2. Update the COM port to match your system:
   ```ini
   [Connection]
   COMPort=COM3  # Change to your COM port
   ```
3. Adjust other settings as needed (baud rate, sensitivity, etc.)
4. Save the file

### Step 6: Connect the Hardware

1. Connect the Twiddler to the USB to Serial adapter
2. Connect the adapter to your computer
3. If using PS/2 power, connect the power adapter
4. Verify the Twiddler powers on (if it has indicator lights)

### Step 7: Test the Connection

Run the driver in test mode:

```cmd
python src/twiddler_driver.py
```

You should see:
```
Twiddler Driver for Windows 11
==================================================

Connected to Twiddler on COM3 at 9600 baud
Twiddler driver started. Press Ctrl+C to exit.
```

Test keyboard input by pressing keys on the Twiddler.
Test mouse movement by moving the Twiddler.

Press Ctrl+C to exit when done testing.

### Step 8: Create a Startup Shortcut (Optional)

To run the driver automatically on Windows startup:

1. Create a batch file `start_twiddler.bat`:
   ```batch
   @echo off
   cd C:\path\to\Twiddler1
   python src/twiddler_driver.py
   ```

2. Create a shortcut to this batch file
3. Move the shortcut to:
   ```
   C:\Users\YourUsername\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
   ```

4. Right-click the shortcut → Properties → Advanced
5. Check "Run as administrator"

## Verification

### Testing Keyboard Input
1. Open Notepad
2. Press keys on the Twiddler
3. Verify characters appear in Notepad
4. Test chord combinations (multiple buttons simultaneously)

### Testing Mouse Input
1. The mouse cursor should move when you manipulate the Twiddler
2. Test mouse button clicks
3. Adjust sensitivity in `config/twiddler.conf` if needed

## Troubleshooting

### Driver Won't Start

**Error: "Failed to connect to COM3"**
- Verify the COM port number in Device Manager
- Update `config/twiddler.conf` with correct COM port
- Check that no other program is using the COM port
- Verify serial adapter is properly connected

**Error: "Required packages not installed"**
- Run: `pip install pyserial keyboard mouse`
- If pip is not found, reinstall Python with "Add to PATH" option

### No Keyboard Input

1. Check Twiddler power and connection
2. Verify COM port in Device Manager
3. Test with serial terminal software first (PuTTY, TeraTerm)
4. Enable debug mode in `config/twiddler.conf`:
   ```ini
   [Advanced]
   DebugMode=True
   ```
5. Check `twiddler.log` for errors

### Mouse Not Working

1. Verify `MouseMode=Enabled` in config
2. Check mouse sensitivity setting
3. Test with debug mode enabled
4. Some Twiddler models may have different mouse protocols

### Permission Errors

**Error: "This driver may require administrator privileges"**
- Run Command Prompt as Administrator
- The keyboard and mouse libraries require admin rights on Windows

### High CPU Usage

- Increase sleep time in the main loop
- Check for excessive debug logging
- Verify baud rate matches Twiddler specifications

## Advanced Configuration

### Customizing Chord Mappings

Edit `config/twiddler.conf` section `[ChordMap]`:

```ini
[ChordMap]
Button1=a
Button1+Button2=e
Button1+Button2+Button3=Space
```

### Adjusting Mouse Sensitivity

```ini
[Mouse]
Sensitivity=1.5  # Increase for faster movement
Acceleration=Enabled
```

### Enabling Debug Mode

For troubleshooting:

```ini
[Advanced]
DebugMode=True
LogFile=twiddler_debug.log
```

## Uninstallation

1. Remove startup shortcut (if created)
2. Stop the driver (Ctrl+C)
3. Uninstall Python packages:
   ```cmd
   pip uninstall pyserial keyboard mouse
   ```
4. Delete the Twiddler1 folder
5. Uninstall serial adapter drivers (optional)

## Support and Resources

### Documentation
- [Hardware Setup Guide](HARDWARE.md)
- [Bluetooth Configuration](BLUETOOTH.md)
- [Protocol Specification](docs/PROTOCOL.md)

### External Resources
- Georgia Tech Bluetooth Twiddler: https://wiki.cc.gatech.edu/ccg/classes/7470/7470-f06/bluetooth_twiddler
- HandyKey Official Site: http://www.handykey.com/
- DIY Wireless Keyboards: http://www.reddit.com/r/MechanicalKeyboards/wiki/wireless-mechanical_keyboards

### Getting Help
- Check `twiddler.log` for error messages
- Enable debug mode for detailed logging
- Verify hardware connections
- Test serial port with terminal software

## Next Steps

1. Customize chord mappings for your workflow
2. Adjust mouse sensitivity for comfort
3. Configure automatic startup
4. Consider Bluetooth modification for wireless operation

Enjoy using your Twiddler with Windows 11!
