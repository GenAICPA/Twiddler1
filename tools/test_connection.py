#!/usr/bin/env python3
"""
Twiddler Connection Test Utility

This utility helps test and debug the connection to the Twiddler device.
It displays raw packet data and validates the serial connection.
"""

import serial
import sys
import time


def test_connection(port='COM3', baudrate=9600):
    """Test serial connection to Twiddler"""
    
    print(f"Twiddler Connection Test Utility")
    print("=" * 50)
    print(f"Port: {port}")
    print(f"Baud Rate: {baudrate}")
    print()
    
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=8,
            stopbits=1,
            parity='N',
            timeout=1
        )
        
        print("✓ Serial port opened successfully")
        print()
        print("Waiting for data... (Press Ctrl+C to exit)")
        print()
        
        packet_count = 0
        
        while True:
            if ser.in_waiting >= 3:
                data = ser.read(3)
                packet_count += 1
                
                # Display packet
                print(f"Packet #{packet_count}: ", end="")
                print(f"[0x{data[0]:02X}, 0x{data[1]:02X}, 0x{data[2]:02X}] ", end="")
                
                # Interpret packet type
                if data[0] == 0x01:
                    print("(Keyboard Event)", end="")
                elif data[0] == 0x02:
                    print("(Mouse Movement)", end="")
                elif data[0] == 0x03:
                    print("(Mouse Button)", end="")
                elif data[0] == 0x00:
                    print("(Idle)", end="")
                elif data[0] == 0xFF:
                    print("(Device Reset)", end="")
                else:
                    print("(Unknown Type)", end="")
                
                print()
                
            time.sleep(0.01)
            
    except serial.SerialException as e:
        print(f"✗ Error opening serial port: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check that the COM port exists in Device Manager")
        print("2. Verify no other program is using the port")
        print("3. Check USB cable and adapter connections")
        return 1
        
    except KeyboardInterrupt:
        print()
        print()
        print(f"Test completed. Received {packet_count} packets.")
        ser.close()
        return 0
        

def list_ports():
    """List available serial ports"""
    try:
        from serial.tools import list_ports
        
        print("Available serial ports:")
        ports = list(list_ports.comports())
        
        if not ports:
            print("  No serial ports found")
        else:
            for port in ports:
                print(f"  {port.device}: {port.description}")
        print()
        
    except ImportError:
        print("Install pyserial to list ports: pip install pyserial")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', 'help']:
            print("Usage: python test_connection.py [COM_PORT] [BAUD_RATE]")
            print()
            print("Examples:")
            print("  python test_connection.py COM3")
            print("  python test_connection.py COM3 9600")
            print("  python test_connection.py --list")
            sys.exit(0)
        elif sys.argv[1] == '--list':
            list_ports()
            sys.exit(0)
        else:
            port = sys.argv[1]
            baudrate = int(sys.argv[2]) if len(sys.argv) > 2 else 9600
            sys.exit(test_connection(port, baudrate))
    else:
        # Default values
        print("No COM port specified. Listing available ports...")
        print()
        list_ports()
        print("Usage: python test_connection.py [COM_PORT]")
        sys.exit(1)
