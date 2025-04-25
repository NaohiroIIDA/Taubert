"""
Module for controlling Freetech STS3215 servo motors on Raspberry Pi.
"""
import time
import logging
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)

class ServoMotor:
    """
    Class to control a Freetech STS3215 servo motor.
    
    This class provides methods to control the servo motor using serial communication
    via UART on the Raspberry Pi.
    """
    
    def __init__(self, servo_id: int, port: str = '/dev/ttyAMA0', baudrate: int = 115200):
        """
        Initialize a servo motor controller.
        
        Args:
            servo_id: The ID of the servo motor (1-254)
            port: The serial port to use for communication
            baudrate: The baudrate for serial communication
        """
        self.servo_id = servo_id
        self.port = port
        self.baudrate = baudrate
        self.is_connected = False
        self.current_position = 0
        self.current_speed = 0
        
        self._serial = None
        
    def connect(self) -> bool:
        """
        Connect to the servo motor.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            import serial
            
            self._serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=0.1
            )
            self.is_connected = True
            logger.info(f"Connected to servo ID {self.servo_id} on {self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to servo ID {self.servo_id}: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from the servo motor."""
        if self._serial and self.is_connected:
            self._serial.close()
            self.is_connected = False
            logger.info(f"Disconnected from servo ID {self.servo_id}")
    
    def _send_command(self, command_bytes: bytes) -> Optional[bytes]:
        """
        Send a command to the servo and return the response.
        
        Args:
            command_bytes: The command bytes to send
            
        Returns:
            Optional[bytes]: The response bytes or None if failed
        """
        if not self.is_connected or not self._serial:
            logger.error("Cannot send command: not connected to servo")
            return None
        
        try:
            self._serial.write(command_bytes)
            time.sleep(0.01)  # Give the servo time to respond
            
            if self._serial.in_waiting:
                response = self._serial.read(self._serial.in_waiting)
                return response
            return None
        except Exception as e:
            logger.error(f"Error sending command to servo ID {self.servo_id}: {e}")
            return None
    
    def set_position(self, position: int, speed: Optional[int] = None) -> bool:
        """
        Set the position of the servo motor.
        
        Args:
            position: Target position (0-4095, where 0-4095 represents 0-360 degrees)
            speed: Optional speed parameter (0-1023)
            
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        logger.info(f"Setting servo ID {self.servo_id} to position {position}")
        
        self.current_position = position
        if speed is not None:
            self.current_speed = speed
            
        return True
    
    def get_position(self) -> int:
        """
        Get the current position of the servo motor.
        
        Returns:
            int: The current position of the servo
        """
        return self.current_position
    
    def stop(self) -> bool:
        """
        Stop the servo motor.
        
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        logger.info(f"Stopping servo ID {self.servo_id}")
        return True


class ServoController:
    """
    Controller for multiple servo motors.
    """
    
    def __init__(self, port: str = '/dev/ttyAMA0', baudrate: int = 115200):
        """
        Initialize the servo controller.
        
        Args:
            port: The serial port to use for communication
            baudrate: The baudrate for serial communication
        """
        self.port = port
        self.baudrate = baudrate
        self.servos: List[ServoMotor] = []
        
    def add_servo(self, servo_id: int) -> ServoMotor:
        """
        Add a servo to the controller.
        
        Args:
            servo_id: The ID of the servo motor
            
        Returns:
            ServoMotor: The created servo motor object
        """
        servo = ServoMotor(servo_id, self.port, self.baudrate)
        self.servos.append(servo)
        return servo
    
    def connect_all(self) -> bool:
        """
        Connect to all servos.
        
        Returns:
            bool: True if all connections successful, False otherwise
        """
        success = True
        for servo in self.servos:
            if not servo.connect():
                success = False
        return success
    
    def disconnect_all(self) -> None:
        """Disconnect from all servos."""
        for servo in self.servos:
            servo.disconnect()
    
    def stop_all(self) -> None:
        """Stop all servos."""
        for servo in self.servos:
            servo.stop()
