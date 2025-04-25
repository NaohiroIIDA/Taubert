"""
Example script demonstrating basic control of Freetech STS3215 motors.
"""
import time
import sys
import logging
import argparse

import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.taubert.motor.servo import STS3215Motor, MotorController

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run a basic motor control demonstration."""
    parser = argparse.ArgumentParser(description='STS3215 Motor Control Example')
    parser.add_argument('--port', type=str, default='/dev/ttyACM0',
                        help='Serial port for motor communication')
    parser.add_argument('--baudrate', type=int, default=115200,
                        help='Baudrate for serial communication')
    parser.add_argument('--motor-ids', type=int, nargs='+', default=[1, 2, 3],
                        help='IDs for the motors to control')
    parser.add_argument('--set-id', type=int, default=0,
                        help='Set a new ID for the first motor (0 to skip)')
    parser.add_argument('--speed', type=int, default=200,
                        help='Speed for motor rotation (0-1023)')
    parser.add_argument('--duration', type=float, default=2.0,
                        help='Duration in seconds for each movement')
    
    args = parser.parse_args()
    
    controller = MotorController(args.port, args.baudrate)
    
    motors = []
    for motor_id in args.motor_ids:
        motor = controller.add_motor(motor_id)
        motors.append(motor)
    
    try:
        logger.info("Connecting to motors...")
        for motor in motors:
            if not motor.connect():
                logger.error(f"Failed to connect to motor ID {motor.motor_id}. Exiting.")
                return
        
        logger.info("Connected to motors successfully")
        
        if args.set_id > 0 and len(motors) > 0:
            logger.info(f"Setting motor ID from {motors[0].motor_id} to {args.set_id}")
            if motors[0].set_id(args.set_id):
                logger.info(f"Successfully set motor ID to {args.set_id}")
                motors[0].motor_id = args.set_id
            else:
                logger.error(f"Failed to set motor ID to {args.set_id}")
        
        logger.info("Starting motor control sequence")
        
        for i, motor in enumerate(motors):
            logger.info(f"Rotating motor ID {motor.motor_id} at speed {args.speed}")
            motor.set_speed(args.speed)
            time.sleep(args.duration)
            motor.stop()
            logger.info(f"Stopped motor ID {motor.motor_id}")
            time.sleep(1)  # Pause between motors
        
        logger.info("Rotating all motors simultaneously")
        for motor in motors:
            motor.set_speed(args.speed)
        
        time.sleep(args.duration)
        
        logger.info("Stopping all motors")
        for motor in motors:
            motor.stop()
        
        logger.info("Motor control sequence completed")
        
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
    finally:
        logger.info("Stopping and disconnecting from all motors")
        for motor in motors:
            motor.stop()
            motor.disconnect()


if __name__ == "__main__":
    main()
