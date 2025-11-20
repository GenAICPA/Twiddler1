# Twiddler Protocol Specification

## Overview
This document describes the serial communication protocol used by the original Twiddler handheld keyboard/mouse device.

## Serial Configuration

### Standard Settings
- **Baud Rate**: 9600 bps (default)
- **Data Bits**: 8
- **Stop Bits**: 1
- **Parity**: None
- **Flow Control**: None

### Alternative Baud Rates
Some Twiddler models may support:
- 4800 bps
- 19200 bps

Consult your Twiddler documentation for model-specific settings.

## Packet Format

### General Structure
The Twiddler sends data in 3-byte packets:

```
Byte 0: Packet Type
Byte 1: Data Byte 1
Byte 2: Data Byte 2
```

### Packet Types

#### 0x01 - Keyboard Event
Indicates a keyboard button press or chord combination.

```
Byte 0: 0x01
Byte 1: Button State (bit flags)
Byte 2: Chord Value
```

**Button State Bit Flags**:
- Bit 0: Button 1
- Bit 1: Button 2
- Bit 2: Button 3
- Bit 3: Button 4
- Bit 4: Modifier (Shift)
- Bit 5: Modifier (Ctrl)
- Bit 6: Modifier (Alt)
- Bit 7: Reserved

**Chord Value**:
- 0x00-0xFF: Represents the chord combination
- Mapping depends on user configuration

#### 0x02 - Mouse Movement
Indicates relative mouse movement.

```
Byte 0: 0x02
Byte 1: X Delta (signed)
Byte 2: Y Delta (signed)
```

**Delta Values**:
- Signed 8-bit integers (-128 to +127)
- Positive X: Move right
- Negative X: Move left
- Positive Y: Move down (standard screen coordinates)
- Negative Y: Move up

#### 0x03 - Mouse Button Event
Indicates mouse button state changes.

```
Byte 0: 0x03
Byte 1: Button State
Byte 2: Reserved (0x00)
```

**Button State**:
- Bit 0: Left button pressed
- Bit 1: Right button pressed
- Bit 2: Middle button pressed
- Bits 3-7: Reserved

### Special Packets

#### 0x00 - Idle/Null Packet
Sent when no input is detected (some models only).

```
Byte 0: 0x00
Byte 1: 0x00
Byte 2: 0x00
```

#### 0xFF - Device Reset
Indicates device initialization or reset.

```
Byte 0: 0xFF
Byte 1: Version byte
Byte 2: Checksum
```

## Chord Encoding

### Basic Principle
The Twiddler uses chording - pressing multiple buttons simultaneously to produce different characters.

### Example Chord Mappings

#### Single Button (A-D)
```
Button 1 alone → 'a' (chord value 0x01)
Button 2 alone → 'b' (chord value 0x02)
Button 3 alone → 'c' (chord value 0x03)
Button 4 alone → 'd' (chord value 0x04)
```

#### Two Button Combinations
```
Button 1 + Button 2 → 'e' (chord value 0x05)
Button 1 + Button 3 → 'f' (chord value 0x06)
Button 1 + Button 4 → 'g' (chord value 0x07)
Button 2 + Button 3 → 'h' (chord value 0x08)
```

#### Three Button Combinations
```
Button 1 + Button 2 + Button 3 → Space (chord value 0x20)
Button 2 + Button 3 + Button 4 → Enter (chord value 0x0D)
```

### Modifier Keys
When modifier buttons (Shift, Ctrl, Alt) are held:
- Bit flags in Byte 1 are set
- Chord value in Byte 2 represents base character
- Host software combines modifiers with character

## Timing Considerations

### Debounce
- Typical debounce time: 5-10 milliseconds
- Handled by Twiddler hardware

### Chord Detection Window
- Time window for detecting simultaneous button presses: ~50 milliseconds
- Buttons pressed within this window are considered a chord

### Key Repeat
- Initial delay: 500 milliseconds (configurable)
- Repeat rate: 30 characters per second (configurable)
- Sent as repeated keyboard packets

## Mouse Protocol Details

### Movement Updates
- Sent approximately 60 times per second during movement
- Resolution: 8-bit signed values
- Acceleration handled by host software

### Button Events
- Sent on button state change (press or release)
- Separate from movement packets

### Coordinate System
```
        -Y (up)
         |
-X (left)|
    -----+-----
         |     +X (right)
         |
        +Y (down)
```

## Error Handling

### Invalid Packets
- Discard packets that don't match expected format
- Log errors for debugging
- Continue reading next packet

### Buffer Overflow
- Clear serial buffer if overflow detected
- Resynchronize packet boundaries

### Timeout
- If no data received for >1 second, assume connection lost
- Attempt reconnection

## Example Packet Sequences

### Typing "Hello"
```
Packet 1: [0x01, 0x08, 0x68]  # 'h' (chord for H)
Packet 2: [0x01, 0x05, 0x65]  # 'e'
Packet 3: [0x01, 0x0C, 0x6C]  # 'l'
Packet 4: [0x01, 0x0C, 0x6C]  # 'l'
Packet 5: [0x01, 0x0F, 0x6F]  # 'o'
```

### Mouse Movement and Click
```
Packet 1: [0x02, 0x05, 0xFE]  # Move right 5, up 2 (-2 = 0xFE)
Packet 2: [0x02, 0x03, 0x00]  # Move right 3, no Y movement
Packet 3: [0x03, 0x01, 0x00]  # Left button press
Packet 4: [0x03, 0x00, 0x00]  # Left button release
```

### Chord with Modifier
```
Packet: [0x01, 0x11, 0x61]  # Shift + 'a' = 'A'
                              # Bit 4 set (0x10) + Button 1 (0x01) = 0x11
                              # Chord value 0x61 ('a')
```

## Implementation Notes

### Reading Serial Data
```python
# Read packets in 3-byte chunks
packet = serial_port.read(3)
packet_type = packet[0]
data1 = packet[1]
data2 = packet[2]
```

### Handling Signed Bytes
```python
def signed_byte(byte):
    """Convert unsigned byte to signed"""
    return byte if byte < 128 else byte - 256
```

### Packet Validation
```python
def is_valid_packet(packet):
    """Validate packet structure"""
    if len(packet) != 3:
        return False
    if packet[0] not in [0x00, 0x01, 0x02, 0x03, 0xFF]:
        return False
    return True
```

## Version Differences

### Twiddler 1 (Original)
- 9600 baud default
- 3-byte packet format
- Limited button count

### Twiddler 2/3
- May use different baud rates
- Extended packet formats
- Additional buttons and features
- Not covered by this specification

## References

For more information:
- Twiddler User Manual (if available)
- Georgia Tech Bluetooth Twiddler Project
- HandyKey Corporation documentation

## Disclaimer

This specification is based on reverse engineering and community documentation. Actual Twiddler models may vary. Always consult official documentation when available.
