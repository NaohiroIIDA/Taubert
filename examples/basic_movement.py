"""
Example script demonstrating basic movement of the Taubert robot.
"""
import time
import sys
import logging

import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.taubert.main import TaubertRobot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run a basic movement demonstration."""
    robot = TaubertRobot()
    
    try:
        logger.info("Connecting to hardware...")
        if not robot.connect():
            logger.error("Failed to connect to hardware. Exiting.")
            return
        
        logger.info("Connected to hardware successfully")
        
        logger.info("Starting movement sequence")
        
        logger.info("Moving forward")
        robot.omni_drive.move_forward(0.5)
        time.sleep(2)
        
        logger.info("Stopping")
        robot.stop()
        time.sleep(1)
        
        logger.info("Moving in a square pattern")
        
        robot.omni_drive.move_forward(0.5)
        time.sleep(1)
        
        robot.omni_drive.move_right(0.5)
        time.sleep(1)
        
        robot.omni_drive.move_backward(0.5)
        time.sleep(1)
        
        robot.omni_drive.move_left(0.5)
        time.sleep(1)
        
        logger.info("Rotating clockwise")
        robot.omni_drive.rotate_clockwise(0.3)
        time.sleep(3)
        
        logger.info("Rotating counterclockwise")
        robot.omni_drive.rotate_counterclockwise(0.3)
        time.sleep(3)
        
        logger.info("Stopping")
        robot.stop()
        
        logger.info("Movement sequence completed")
        
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
