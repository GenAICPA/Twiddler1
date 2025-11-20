#!/usr/bin/env python3
"""
Twiddler Serial to USB HID Driver for Windows 11

This driver translates serial input from the Twiddler handheld keyboard/mouse
to USB HID events that Windows 11 can understand.

Requirements:
- Python 3.7+
- pyserial
- keyboard (for keyboard emulation)
- mouse (for mouse emulation)

Install dependencies:
    pip install pyserial keyboard mouse
"""

import serial
import time
import configparser
import logging
import sys
import os
from pathlib import Path

try:
    import keyboard
    import mouse
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install pyserial keyboard mouse")
    sys.exit(1)


class TwiddlerDriver:
    """Main driver class for Twiddler device"""
    
    def __init__(self, config_file='config/twiddler.conf'):
        """Initialize the driver with configuration"""
        self.config = configparser.ConfigParser()
        self.load_config(config_file)
        self.serial_port = None
        self.running = False
        self.setup_logging()
        
    def load_config(self, config_file):
        """Load configuration from file"""
        if not os.path.exists(config_file):
            print(f"Config file not found: {config_file}")
            print("Creating default configuration...")
            self.create_default_config(config_file)
        
        self.config.read(config_file)
        
    def create_default_config(self, config_file):
        """Create default configuration file"""
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        config = configparser.ConfigParser()
        config['Connection'] = {
            'Type': 'USB',
            'COMPort': 'COM3',
            'BaudRate': '9600',
            'DataBits': '8',
            'StopBits': '1',
            'Parity': 'None'
        }
        config['Device'] = {
            'Model': 'Twiddler1',
            'ChordingMode': 'Enabled',
            'MouseMode': 'Enabled'
        }
        
        with open(config_file, 'w') as f:
            config.write(f)
            
    def setup_logging(self):
        """Setup logging configuration"""
        debug_mode = self.config.getboolean('Advanced', 'DebugMode', fallback=False)
        log_file = self.config.get('Advanced', 'LogFile', fallback='twiddler.log')
        
        level = logging.DEBUG if debug_mode else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def connect(self):
        """Connect to the Twiddler device via serial port"""
        port = self.config.get('Connection', 'COMPort')
        baud_rate = self.config.getint('Connection', 'BaudRate')
        
        try:
            self.serial_port = serial.Serial(
                port=port,
                baudrate=baud_rate,
                bytesize=self.config.getint('Connection', 'DataBits'),
                stopbits=self.config.getint('Connection', 'StopBits'),
                timeout=self.config.getfloat('Advanced', 'Timeout', fallback=1000) / 1000
            )
            self.logger.info(f"Connected to Twiddler on {port} at {baud_rate} baud")
            return True
        except serial.SerialException as e:
            self.logger.error(f"Failed to connect to {port}: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from the Twiddler device"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.logger.info("Disconnected from Twiddler")
            
    def parse_packet(self, data):
        """Parse a data packet from the Twiddler
        
        The Twiddler sends data in packets. This method interprets the packet
        and returns the event type and data.
        
        Packet format (example for original Twiddler):
        - Byte 0: Packet type (0x01 = keyboard, 0x02 = mouse)
        - Byte 1-2: Data bytes
        
        Returns:
            tuple: (event_type, event_data)
        """
        if len(data) < 3:
            return None, None
            
        packet_type = data[0]
        
        if packet_type == 0x01:  # Keyboard event
            # Parse keyboard data
            button_state = data[1]
            chord_value = data[2]
            return 'keyboard', {'buttons': button_state, 'chord': chord_value}
        elif packet_type == 0x02:  # Mouse event
            # Parse mouse data
            x_delta = self.signed_byte(data[1])
            y_delta = self.signed_byte(data[2])
            return 'mouse', {'dx': x_delta, 'dy': y_delta}
        elif packet_type == 0x03:  # Mouse button event
            button_state = data[1]
            return 'mouse_button', {'buttons': button_state}
            
        return None, None
        
    @staticmethod
    def signed_byte(byte):
        """Convert unsigned byte to signed byte"""
        return byte if byte < 128 else byte - 256
        
    def process_keyboard_event(self, event_data):
        """Process keyboard event and send to system"""
        buttons = event_data['buttons']
        chord = event_data['chord']
        
        # Map chord to character (simplified example)
        # In a real implementation, this would use the ChordMap from config
        char = self.map_chord_to_char(buttons, chord)
        
        if char:
            self.logger.debug(f"Keyboard: {char}")
            try:
                keyboard.write(char)
            except Exception as e:
                self.logger.error(f"Error sending keyboard input: {e}")
                
    def process_mouse_event(self, event_data):
        """Process mouse movement event"""
        dx = event_data['dx']
        dy = event_data['dy']
        
        # Apply sensitivity from config
        sensitivity = self.config.getfloat('Mouse', 'Sensitivity', fallback=1.0)
        dx = int(dx * sensitivity)
        dy = int(dy * sensitivity)
        
        self.logger.debug(f"Mouse move: dx={dx}, dy={dy}")
        try:
            mouse.move(dx, dy, absolute=False)
        except Exception as e:
            self.logger.error(f"Error sending mouse movement: {e}")
            
    def process_mouse_button_event(self, event_data):
        """Process mouse button event"""
        buttons = event_data['buttons']
        
        # Bit 0: Left button
        # Bit 1: Right button
        # Bit 2: Middle button
        
        if buttons & 0x01:
            self.logger.debug("Mouse: Left click")
            mouse.click('left')
        if buttons & 0x02:
            self.logger.debug("Mouse: Right click")
            mouse.click('right')
        if buttons & 0x04:
            self.logger.debug("Mouse: Middle click")
            mouse.click('middle')
            
    def map_chord_to_char(self, buttons, chord):
        """Map button combination to character
        
        This is a simplified example. A full implementation would:
        1. Read chord mappings from config file
        2. Support multi-button chording
        3. Handle modifier keys
        """
        # Example basic mapping
        chord_map = {
            0x01: 'a', 0x02: 'b', 0x03: 'c', 0x04: 'd',
            0x05: 'e', 0x06: 'f', 0x07: 'g', 0x08: 'h',
            0x20: ' ',  # Space
            0x0D: '\n', # Enter
        }
        
        return chord_map.get(chord, None)
        
    def run(self):
        """Main event loop"""
        if not self.connect():
            return
            
        self.running = True
        self.logger.info("Twiddler driver started. Press Ctrl+C to exit.")
        
        packet_size = self.config.getint('Advanced', 'PacketSize', fallback=3)
        
        try:
            while self.running:
                if self.serial_port.in_waiting >= packet_size:
                    data = self.serial_port.read(packet_size)
                    
                    event_type, event_data = self.parse_packet(data)
                    
                    if event_type == 'keyboard':
                        self.process_keyboard_event(event_data)
                    elif event_type == 'mouse':
                        self.process_mouse_event(event_data)
                    elif event_type == 'mouse_button':
                        self.process_mouse_button_event(event_data)
                        
                time.sleep(0.001)  # Small delay to prevent CPU spinning
                
        except KeyboardInterrupt:
            self.logger.info("Shutting down...")
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
        finally:
            self.disconnect()
            

def main():
    """Main entry point"""
    print("Twiddler Driver for Windows 11")
    print("=" * 50)
    print()
    
    # Check for admin rights (required for keyboard/mouse emulation)
    if sys.platform == 'win32':
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print("Warning: This driver may require administrator privileges")
                print("to emulate keyboard and mouse input.")
                print()
        except:
            pass
    
    config_file = 'config/twiddler.conf'
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    
    driver = TwiddlerDriver(config_file)
    driver.run()


if __name__ == '__main__':
    main()
