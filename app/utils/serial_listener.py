import serial
import time
import logging

SERIAL_PORT = 'COM9'
BAUD_RATE = 115200

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def wait_for_trigger():
    """
    Opens serial port, waits for 'motion', then returns True.
    Keeps the port open for 'resume' command later.
    """
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        logging.info(f"🔌 Listening to serial port {SERIAL_PORT} for 'motion'...")

        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip().lower()
            if line:
                logging.info(f"📨 Received: {line}")
            if "motion" in line:
                logging.info("🎯 Motion detected via ESP!")
                return ser  # Keep serial open for sending 'resume'

    except serial.SerialException as e:
        logging.error(f"❌ Serial connection error: {e}")
        return None
    except KeyboardInterrupt:
        logging.info("\n🚪 Exiting via Ctrl+C")
        return None
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            logging.info(f"🔒 Closed serial port {SERIAL_PORT}")
