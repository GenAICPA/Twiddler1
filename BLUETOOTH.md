# Bluetooth Setup Guide

## Overview
This guide describes how to add Bluetooth capability to the original Twiddler device for wireless operation with Windows 11.

## Prerequisites
- Twiddler device with 9-pin serial port
- Bluetooth Serial Port Profile (SPP) module
- Basic soldering skills (for hardware modification)
- Windows 11 computer with Bluetooth capability

## Hardware Modification

### Required Components
1. **Bluetooth Serial Module**
   - BlueSMiRF Silver/Gold (recommended)
   - Or HC-05/HC-06 Bluetooth module
   - Voltage regulator if module requires 3.3V and Twiddler outputs 5V

2. **Connector Components**
   - DB-9 connector (female) for Twiddler connection
   - Wires for connections
   - Heat shrink tubing

### Wiring Connections
Connect the Bluetooth module to Twiddler's serial port:

```
Twiddler DB-9    Bluetooth Module
Pin 2 (TX)   →   RX (Receive)
Pin 3 (RX)   →   TX (Transmit)
Pin 5 (GND)  →   GND (Ground)
Pin 9 (5V)*  →   VCC (Power)**
```

\* Check your Twiddler model for power pin location
\** Use voltage regulator if module requires 3.3V

### Assembly Steps
1. Open the Bluetooth module enclosure
2. Solder wires to TX, RX, GND, and VCC pins
3. Connect wires to DB-9 connector following the pin diagram above
4. Use voltage regulator between Twiddler power and module if needed
5. Insulate connections with heat shrink tubing
6. Test connections with multimeter
7. Secure assembly in protective enclosure

## Bluetooth Configuration

### Pairing with Windows 11
1. Power on the Bluetooth module
2. Open Windows Settings → Bluetooth & devices
3. Click "Add device" → "Bluetooth"
4. Select your Bluetooth serial module from the list
5. Enter pairing PIN if required (often "0000" or "1234")
6. Wait for successful pairing confirmation

### Virtual COM Port Setup
1. Open Device Manager (Win + X → Device Manager)
2. Expand "Bluetooth" section
3. Right-click on paired device → Properties
4. Go to "Services" tab
5. Enable "Serial Port" service
6. Note the assigned COM port number (e.g., COM7)

### Alternative: Bluetooth SPP Settings
If virtual COM port doesn't appear automatically:
1. Download and install Bluetooth SPP software from module manufacturer
2. Configure incoming COM port
3. Set baud rate to match Twiddler (typically 9600 bps)
4. Set data bits: 8, Stop bits: 1, Parity: None

## Software Configuration

### Configure Twiddler Driver
Edit `config/twiddler.conf`:
```
[Connection]
Type=Bluetooth
COMPort=COM7
BaudRate=9600
DataBits=8
StopBits=1
Parity=None
```

### Testing Connection
1. Run the Twiddler driver software (see INSTALL.md)
2. Check connection status in the console
3. Test keyboard input by pressing Twiddler keys
4. Test mouse movement
5. Verify chord recognition

## Bluetooth Module Configuration

### BlueSMiRF Configuration
Default settings are usually correct, but to modify:
1. Connect module via USB-to-serial adapter
2. Use terminal software (PuTTY, Arduino Serial Monitor)
3. Enter command mode: `$$$`
4. Set baud rate: `U,9600,N` (9600 baud, no parity)
5. Set device name: `SN,Twiddler`
6. Exit command mode: `---`

### HC-05/HC-06 Configuration
1. Connect module in AT command mode
2. Use terminal software at 38400 baud (HC-05) or 9600 baud (HC-06)
3. Configure baud rate: `AT+UART=9600,0,0`
4. Set device name: `AT+NAME=Twiddler`
5. Set PIN: `AT+PSWD=1234`

## Troubleshooting

### Pairing Issues
- Ensure Bluetooth module is powered and in discoverable mode
- Reset Bluetooth module to factory settings
- Clear old pairings from Windows Bluetooth settings
- Try pairing from different location (reduce interference)

### Connection Drops
- Check power supply stability
- Reduce distance between device and computer
- Minimize interference from other 2.4GHz devices
- Update Bluetooth drivers on Windows 11

### Data Loss or Corruption
- Verify baud rate matches on both sides
- Check for loose wire connections
- Test with shorter distance first
- Reduce data transmission rate if necessary

### Power Consumption
- Bluetooth modules consume more power than wired connection
- Consider external battery pack for extended use
- Some modules have power-saving modes (consult documentation)

## Power Management

### Battery Operation
For portable use:
- Use rechargeable battery pack (3.7V LiPo with boost converter)
- Add charging circuit for convenience
- Monitor battery voltage to prevent over-discharge
- Typical operation time: 8-12 hours depending on battery capacity

### Power Switch
Add a toggle switch between battery and Bluetooth module for power management.

## Safety Considerations
- Double-check voltage levels before connecting
- Use properly rated voltage regulators
- Insulate all connections to prevent shorts
- Test with multimeter before final assembly
- Avoid connecting reversed polarity

## References
- Georgia Tech Bluetooth Twiddler Project: https://wiki.cc.gatech.edu/ccg/classes/7470/7470-f06/bluetooth_twiddler
- Twiddler Official Site: http://www.handykey.com/
- DIY Wireless Keyboard Modifications: http://www.reddit.com/r/MechanicalKeyboards/wiki/wireless-mechanical_keyboards
