"""
Module for controlling omnidirectional movement with three omni-wheels.
"""
import math
import logging
from typing import List, Tuple, Optional
from ..motor.servo import ServoMotor, ServoController

logger = logging.getLogger(__name__)

class OmniDrive:
    """
    Class to control omnidirectional movement with three omni-wheels.
    
    The wheels are positioned at 120-degree intervals (0, 120, 240 degrees).
    """
    
    def __init__(self, servo_controller: ServoController, servo_ids: List[int], wheel_radius: float = 0.05):
        """
        Initialize the omnidirectional drive system.
        
        Args:
            servo_controller: The servo controller object
            servo_ids: List of three servo IDs for the omni-wheels
            wheel_radius: Radius of the omni-wheels in meters
        """
        if len(servo_ids) != 3:
            raise ValueError("OmniDrive requires exactly 3 servo IDs")
        
        self.servo_controller = servo_controller
        self.servos = [servo_controller.add_servo(servo_id) for servo_id in servo_ids]
        self.wheel_radius = wheel_radius
        
        self.wheel_angles = [0, 2*math.pi/3, 4*math.pi/3]
        
        self.max_speed = 1023  # Maximum speed value for the servos
        
    def connect(self) -> bool:
        """
        Connect to all servo motors.
        
        Returns:
            bool: True if all connections successful, False otherwise
        """
        return self.servo_controller.connect_all()
    
    def disconnect(self) -> None:
        """Disconnect from all servo motors."""
        self.servo_controller.disconnect_all()
    
    def stop(self) -> None:
        """Stop all motors."""
        self.servo_controller.stop_all()
        logger.info("Stopped all motors")
    
    def calculate_wheel_speeds(self, vx: float, vy: float, omega: float) -> List[int]:
        """
        Calculate the required wheel speeds for the desired motion.
        
        Args:
            vx: Desired velocity in the x direction (-1.0 to 1.0)
            vy: Desired velocity in the y direction (-1.0 to 1.0)
            omega: Desired angular velocity (-1.0 to 1.0)
            
        Returns:
            List[int]: List of wheel speeds for each servo
        """
        vx = max(-1.0, min(1.0, vx))
        vy = max(-1.0, min(1.0, vy))
        omega = max(-1.0, min(1.0, omega))
        
        wheel_speeds = []
        for angle in self.wheel_angles:
            wheel_speed = vx * math.cos(angle) + vy * math.sin(angle) + omega
            
            scaled_speed = int(wheel_speed * self.max_speed)
            
            scaled_speed = max(-self.max_speed, min(self.max_speed, scaled_speed))
            
            wheel_speeds.append(scaled_speed)
        
        return wheel_speeds
    
    def move(self, vx: float, vy: float, omega: float) -> bool:
        """
        Move the robot with the specified velocities.
        
        Args:
            vx: Desired velocity in the x direction (-1.0 to 1.0)
            vy: Desired velocity in the y direction (-1.0 to 1.0)
            omega: Desired angular velocity (-1.0 to 1.0)
            
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        wheel_speeds = self.calculate_wheel_speeds(vx, vy, omega)
        
        success = True
        for i, servo in enumerate(self.servos):
            
            speed = abs(wheel_speeds[i])
            position = 2048 + (wheel_speeds[i] // 2)
            
            if not servo.set_position(position, speed):
                success = False
        
        if success:
            logger.info(f"Moving with vx={vx}, vy={vy}, omega={omega}, wheel_speeds={wheel_speeds}")
        else:
            logger.error(f"Failed to move with vx={vx}, vy={vy}, omega={omega}")
        
        return success
    
    def move_forward(self, speed: float = 0.5) -> bool:
        """
        Move the robot forward.
        
        Args:
            speed: Speed from 0.0 to 1.0
            
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        return self.move(0, speed, 0)
    
    def move_backward(self, speed: float = 0.5) -> bool:
        """
        Move the robot backward.
        
        Args:
            speed: Speed from 0.0 to 1.0
            
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        return self.move(0, -speed, 0)
    
    def move_left(self, speed: float = 0.5) -> bool:
        """
        Move the robot to the left.
        
        Args:
            speed: Speed from 0.0 to 1.0
            
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        return self.move(-speed, 0, 0)
    
    def move_right(self, speed: float = 0.5) -> bool:
        """
        Move the robot to the right.
        
        Args:
            speed: Speed from 0.0 to 1.0
            
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        return self.move(speed, 0, 0)
    
    def rotate_clockwise(self, speed: float = 0.5) -> bool:
        """
        Rotate the robot clockwise.
        
        Args:
            speed: Speed from 0.0 to 1.0
            
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        return self.move(0, 0, speed)
    
    def rotate_counterclockwise(self, speed: float = 0.5) -> bool:
        """
        Rotate the robot counterclockwise.
        
        Args:
            speed: Speed from 0.0 to 1.0
            
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        return self.move(0, 0, -speed)
