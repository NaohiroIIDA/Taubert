"""
Main module for the Taubert robot control.
"""
import time
import logging
import argparse
from typing import List, Optional

from .motor.servo import ServoController
from .movement.omni_drive import OmniDrive

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TaubertRobot:
    """
    Main class for controlling the Taubert robot.
    """
    
    def __init__(self, servo_ids: List[int] = [1, 2, 3], port: str = '/dev/ttyAMA0', baudrate: int = 115200):
        """
        Initialize the Taubert robot.
        
        Args:
            servo_ids: List of servo IDs for the three motors
            port: Serial port for communication with the servos
            baudrate: Baudrate for serial communication
        """
        self.servo_controller = ServoController(port, baudrate)
        self.omni_drive = OmniDrive(self.servo_controller, servo_ids)
        
    def connect(self) -> bool:
        """
        Connect to all hardware components.
        
        Returns:
            bool: True if all connections successful, False otherwise
        """
        return self.omni_drive.connect()
    
    def disconnect(self) -> None:
        """Disconnect from all hardware components."""
        self.omni_drive.disconnect()
    
    def stop(self) -> None:
        """Stop all motors."""
        self.omni_drive.stop()
    
    def demo_movement(self, duration: float = 1.0) -> None:
        """
        Demonstrate basic movement capabilities.
        
        Args:
            duration: Duration in seconds for each movement
        """
        logger.info("Starting movement demonstration")
        
        logger.info("Moving forward")
        self.omni_drive.move_forward(0.5)
        time.sleep(duration)
        
        logger.info("Moving backward")
        self.omni_drive.move_backward(0.5)
        time.sleep(duration)
        
        logger.info("Moving left")
        self.omni_drive.move_left(0.5)
        time.sleep(duration)
        
        logger.info("Moving right")
        self.omni_drive.move_right(0.5)
        time.sleep(duration)
        
        logger.info("Rotating clockwise")
        self.omni_drive.rotate_clockwise(0.5)
        time.sleep(duration)
        
        logger.info("Rotating counterclockwise")
        self.omni_drive.rotate_counterclockwise(0.5)
        time.sleep(duration)
        
        self.stop()
        logger.info("Movement demonstration completed")


def main():
    """Main entry point for the Taubert robot control."""
    parser = argparse.ArgumentParser(description='Taubert Robot Control')
    parser.add_argument('--port', type=str, default='/dev/ttyAMA0',
                        help='Serial port for servo communication')
    parser.add_argument('--baudrate', type=int, default=115200,
                        help='Baudrate for serial communication')
    parser.add_argument('--servo-ids', type=int, nargs=3, default=[1, 2, 3],
                        help='IDs for the three servo motors')
    parser.add_argument('--demo', action='store_true',
                        help='Run a movement demonstration')
    
    args = parser.parse_args()
    
    robot = TaubertRobot(args.servo_ids, args.port, args.baudrate)
    
    try:
        if not robot.connect():
            logger.error("Failed to connect to hardware. Exiting.")
            return
        
        logger.info("Connected to hardware successfully")
        
        if args.demo:
            robot.demo_movement()
        else:
            logger.info("No action specified. Use --demo to run a movement demonstration.")
            
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
    finally:
        robot.stop()
        robot.disconnect()
        logger.info("Disconnected from hardware")


if __name__ == "__main__":
    main()
