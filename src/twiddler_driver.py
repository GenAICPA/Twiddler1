import serial
import time
import configparser
import os
import sys
import logging
import platform

# Conditional import for keyboard and mouse libraries
# These libraries typically require administrator privileges on Windows
try:
    import keyboard
    import mouse
    HAS_KEYBOARD_MOUSE = True
except ImportError:
    HAS_KEYBOARD_MOUSE = False
    print("Warning: 'keyboard' and 'mouse' libraries not found. Keyboard/mouse emulation will be disabled.")
    print("Please install them using: pip install keyboard mouse")
    print("On Windows, you might need to run as Administrator for full functionality.")

# --- Configuration ---
CONFIG_FILE = 'config/twiddler.conf'
DEFAULT_CONFIG = {
    'Connection': {
        'COMPort': 'COM3',
        'BaudRate': '9600',
        'Timeout': '0.1'
    },
    'Device': {
        'Model': 'Twiddler1',
        'ChordingMode': 'Standard',
        'MouseMode': 'Enabled'
    },
    'Mouse': {
        'Sensitivity': '1.0',
        'Acceleration': 'Enabled'
    },
    'Advanced': {
        'DebugMode': 'False',
        'LogFile': 'twiddler.log'
    }
}

# --- Logging Setup ---
def setup_logging(debug_mode, log_file):
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logging.basicConfig(level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler(sys.stdout)
                        ])

# --- Helper Functions ---
def is_admin():
    if platform.system() == "Windows":
        try:
            return os.getuid() == 0
        except AttributeError:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
    else:
        return os.getuid() == 0 # Check for root on Linux/macOS

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists('config'):
        os.makedirs('config')
    
    if not os.path.exists(CONFIG_FILE):
        logging.info(f"Creating default config file: {CONFIG_FILE}")
        for section, options in DEFAULT_CONFIG.items():
            config.add_section(section)
            for key, value in options.items():
                config.set(section, key, value)
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
    else:
        config.read(CONFIG_FILE)
    return config

def map_chord_to_char(chord_value):
    # This is a simplified example. A full implementation would
    # read chord mappings from config, support multi-button chording,
    # and handle modifier keys.
    if chord_value == 0b00001: return 'a'
    if chord_value == 0b00010: return 'b'
    if chord_value == 0b00100: return 'c'
    if chord_value == 0b01000: return 'd'
    if chord_value == 0b10000: return 'e'
    # Add more mappings as needed
    return None

# --- Twiddler Driver Class ---
class TwiddlerDriver:
    def __init__(self, config):
        self.config = config
        self.port = config.get('Connection', 'COMPort')
        self.baudrate = config.getint('Connection', 'BaudRate')
        self.timeout = config.getfloat('Connection', 'Timeout')
        self.mouse_sensitivity = config.getfloat('Mouse', 'Sensitivity')
        self.mouse_acceleration = config.get('Mouse', 'Acceleration').lower() == 'enabled'
        self.mouse_mode = config.get('Device', 'MouseMode').lower() == 'enabled'
        self.serial_connection = None
        self.last_x = 0
        self.last_y = 0

    def connect(self):
        try:
            self.serial_connection = serial.Serial(
                self.port,
                self.baudrate,
                timeout=self.timeout
            )
            # Explicitly clear DTR line as Twiddler only transmits when DTR is low
            self.serial_connection.setDTR(False)
            logging.info(f"Connected to Twiddler on {self.port} at {self.baudrate} baud")
            return True
        except serial.SerialException as e:
            logging.error(f"Failed to connect to {self.port}: {e}")
            return False

    def disconnect(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            logging.info("Disconnected from Twiddler.")

    def process_packet(self, packet):
        if not packet:
            return

        packet_type = packet[0]

        if packet_type == 0x01:  # Keyboard Event
            if len(packet) >= 3:
                button_state = packet[1] # Not currently used, but could indicate press/release
                chord_value = packet[2]
                char = map_chord_to_char(chord_value)
                if char and HAS_KEYBOARD_MOUSE:
                    logging.debug(f"Keyboard: Chord {chord_value:05b} -> '{char}'")
                    keyboard.write(char)
                elif not HAS_KEYBOARD_MOUSE:
                    logging.debug(f"Keyboard event (chord {chord_value:05b}) received, but keyboard emulation is disabled.")
            else:
                logging.warning(f"Malformed keyboard packet: {packet.hex()}")

        elif packet_type == 0x02:  # Mouse Movement
            if self.mouse_mode and HAS_KEYBOARD_MOUSE and len(packet) >= 3:
                delta_x = packet[1] if packet[1] < 128 else packet[1] - 256
                delta_y = packet[2] if packet[2] < 128 else packet[2] - 256

                # Apply sensitivity
                move_x = int(delta_x * self.mouse_sensitivity)
                move_y = int(delta_y * self.mouse_sensitivity)

                # Basic acceleration (optional)
                if self.mouse_acceleration:
                    if abs(delta_x) > 10: move_x *= 2
                    if abs(delta_y) > 10: move_y *= 2
                
                if move_x != 0 or move_y != 0:
                    logging.debug(f"Mouse Move: dx={delta_x}, dy={delta_y} -> mx={move_x}, my={move_y}")
                    mouse.move(move_x, move_y, absolute=False)
            elif not HAS_KEYBOARD_MOUSE:
                logging.debug(f"Mouse movement event received, but mouse emulation is disabled.")
            elif not self.mouse_mode:
                logging.debug(f"Mouse movement event received, but mouse mode is disabled in config.")
            else:
                logging.warning(f"Malformed mouse movement packet: {packet.hex()}")

        elif packet_type == 0x03:  # Mouse Button
            if self.mouse_mode and HAS_KEYBOARD_MOUSE and len(packet) >= 2:
                button_state = packet[1]
                # Assuming button_state is a bitmask:
                # Bit 0: Left Button
                # Bit 1: Right Button
                # Bit 2: Middle Button
                
                if button_state & 0x01: # Left button pressed
                    logging.debug("Mouse Button: Left Click")
                    mouse.click('left')
                if button_state & 0x02: # Right button pressed
                    logging.debug("Mouse Button: Right Click")
                    mouse.click('right')
                if button_state & 0x04: # Middle button pressed
                    logging.debug("Mouse Button: Middle Click")
                    mouse.click('middle')
            elif not HAS_KEYBOARD_MOUSE:
                logging.debug(f"Mouse button event received, but mouse emulation is disabled.")
            elif not self.mouse_mode:
                logging.debug(f"Mouse button event received, but mouse mode is disabled in config.")
            else:
                logging.warning(f"Malformed mouse button packet: {packet.hex()}")
        else:
            logging.warning(f"Unknown packet type: {packet_type:02x} - {packet.hex()}")

    def run(self):
        if not self.connect():
            return

        logging.info("Twiddler driver started. Press Ctrl+C to exit.")
        try:
            while True:
                # Read up to 3 bytes (max packet size for current implementation)
                # The Twiddler sends variable length packets, typically 2-3 bytes.
                # We read a small amount and then process.
                packet = self.serial_connection.read(3) 
                if packet:
                    self.process_packet(packet)
                time.sleep(0.01) # Small delay to prevent high CPU usage
        except KeyboardInterrupt:
            logging.info("Driver stopped by user.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        finally:
            self.disconnect()

# --- Main Execution ---
if __name__ == "__main__":
    print("Twiddler Driver for Windows 11")
    print("==================================================")

    if platform.system() == "Windows" and not is_admin():
        print("Warning: This driver may require administrator privileges for full keyboard/mouse emulation.")
        print("Please run this script as Administrator if you encounter issues.")
        # sys.exit(1) # Don't exit, just warn

    if not HAS_KEYBOARD_MOUSE:
        print("\nERROR: Required 'keyboard' and 'mouse' libraries are not installed or accessible.")
        print("Please install them using: pip install keyboard mouse")
        print("Exiting.")
        sys.exit(1)

    config = load_config()
    debug_mode = config.getboolean('Advanced', 'DebugMode')
    log_file = config.get('Advanced', 'LogFile')
    setup_logging(debug_mode, log_file)

    driver = TwiddlerDriver(config)
    driver.run()
