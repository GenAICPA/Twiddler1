# Hardware Requirements

## Twiddler Device
The original Twiddler handheld keyboard/mouse (1990s era) features:
- 9-pin serial port (DB-9 connector)
- PS/2 keyboard passthrough ports for power
- Chording keyboard interface
- Integrated mouse functionality

## Required Adapters

### Option 1: USB Connection (Recommended)
To connect the Twiddler to a modern Windows 11 computer via USB, you will need:

1. **Serial to USB Adapter**
   - FTDI-based USB to RS-232 serial adapter (recommended for best compatibility)
   - **Ensure the adapter and its drivers support DTR (Data Terminal Ready) line control, as the Twiddler requires DTR to be clear for data transmission.**
   - Example: FTDI USB-to-Serial Cable or similar
   - Ensure Windows 11 drivers are available
   - Supported chipsets: FTDI FT232, Prolific PL2303, or Silicon Labs CP2102

2. **9-Pin Serial Cable**
   - DB-9 male to female cable if needed
   - Ensure proper null-modem configuration if required

3. **PS/2 Power Supply** (if Twiddler requires external power)
   - **The Twiddler typically requires 5V power, originally supplied via a PS/2 keyboard passthrough. For modern systems without PS/2 ports, you will need an external power solution.**
   - PS/2 to USB adapter for power only (ensure it provides 5V)
   - Or powered USB hub (if the USB-to-Serial adapter can draw power from it and pass it to the Twiddler, or if a separate power injector is used)

### Option 2: Bluetooth Connection (Advanced)
For wireless operation:

1. **Bluetooth Serial Adapter**
   - Bluetooth SPP (Serial Port Profile) module
   - Examples: 
     - BlueSMiRF Silver or Gold (SparkFun)
     - HC-05 or HC-06 Bluetooth module
   - Requires modification to Twiddler serial port

2. **Bluetooth Configuration**
   - Pair the Bluetooth serial module with Windows 11
   - Configure as virtual COM port
   - See BLUETOOTH.md for detailed setup

## Hardware Setup

### USB Connection Steps
1. Connect the serial to USB adapter to your computer
2. Install the adapter drivers (usually automatic on Windows 11)
3. Identify the COM port assigned (Device Manager → Ports)
4. Connect the Twiddler's 9-pin serial connector to the adapter
5. If needed, connect PS/2 power supply
6. Note the COM port number for software configuration

### Power Considerations
- Some Twiddler models draw power from the PS/2 keyboard port
- Use a PS/2 to USB adapter or powered hub if external power is needed
- Verify voltage requirements (typically 5V)

## Troubleshooting

### Serial Adapter Not Recognized
- Install manufacturer drivers for the USB-to-serial adapter
- Check Windows Update for automatic driver installation
- Verify adapter is functioning with another serial device

### Power Issues
- Ensure PS/2 power adapter is providing adequate voltage
- Check Twiddler battery (if battery-powered model)
- Test with different power sources

### Data Transmission Issues
- Verify baud rate settings (typically 9600 bps for Twiddler)
- Check for null-modem requirement
- Test serial connection with terminal software first
