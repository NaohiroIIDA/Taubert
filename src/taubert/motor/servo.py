"""
Module for controlling Freetech STS3215 servo motors on Raspberry Pi.
"""
import time
import logging
import serial
from typing import Optional, List, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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


class STS3215Motor:
    """
    Class to control a Freetech STS3215 servo motor via /dev/ttyACM0.
    
    This class provides methods to control the STS3215 servo motor using serial communication
    via /dev/ttyACM0 on the Raspberry Pi.
    """
    
    CMD_WRITE_ID = 0x01
    CMD_SET_POSITION = 0x03
    CMD_SET_SPEED = 0x05
    CMD_READ_POSITION = 0x02
    CMD_READ_SPEED = 0x04
    CMD_STOP = 0x06
    
    def __init__(self, motor_id: int = 1, port: str = '/dev/ttyACM0', baudrate: int = 115200):
        """
        Initialize a STS3215 motor controller.
        
        Args:
            motor_id: The ID of the motor (1-254)
            port: The serial port to use for communication
            baudrate: The baudrate for serial communication
        """
        self.motor_id = motor_id
        self.port = port
        self.baudrate = baudrate
        self.is_connected = False
        self.current_position = 0
        self.current_speed = 0
        self._serial = None
        
    def connect(self) -> bool:
        """
        Connect to the motor.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self._serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=0.1
            )
            self.is_connected = True
            logger.info(f"Connected to motor ID {self.motor_id} on {self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to motor ID {self.motor_id}: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from the motor."""
        if self._serial and self.is_connected:
            self._serial.close()
            self.is_connected = False
            logger.info(f"Disconnected from motor ID {self.motor_id}")
    
    def _calculate_checksum(self, data: bytes) -> int:
        """
        Calculate the checksum for the command.
        
        Args:
            data: The command data bytes
            
        Returns:
            int: The calculated checksum
        """
        return sum(data) % 256
    
    def _send_command(self, command: int, data: bytes = b'') -> Optional[bytes]:
        """
        Send a command to the motor and return the response.
        
        Args:
            command: The command code
            data: The command data bytes
            
        Returns:
            Optional[bytes]: The response bytes or None if failed
        """
        if not self.is_connected or not self._serial:
            logger.error("Cannot send command: not connected to motor")
            return None
        
        try:
            length = len(data) + 2  # command byte + checksum byte
            packet = bytearray([0xFF, 0xFF, self.motor_id, length, command])
            packet.extend(data)
            
            checksum = self._calculate_checksum(packet[2:])  # Skip the header bytes
            packet.append(checksum)
            
            self._serial.write(packet)
            self._serial.flush()
            time.sleep(0.01)  # Give the motor time to respond
            
            if self._serial.in_waiting:
                response = self._serial.read(self._serial.in_waiting)
                return response
            return None
        except Exception as e:
            logger.error(f"Error sending command to motor ID {self.motor_id}: {e}")
            return None
    
    def set_id(self, new_id: int) -> bool:
        """
        Set a new ID for the motor.
        
        Args:
            new_id: The new ID to set (1-254)
            
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        if new_id < 1 or new_id > 254:
            logger.error(f"Invalid motor ID: {new_id}. Must be between 1 and 254.")
            return False
        
        logger.info(f"Setting motor ID from {self.motor_id} to {new_id}")
        
        data = bytes([new_id])
        response = self._send_command(self.CMD_WRITE_ID, data)
        
        if response:
            self.motor_id = new_id
            logger.info(f"Successfully changed motor ID to {new_id}")
            return True
        else:
            logger.error(f"Failed to change motor ID to {new_id}")
            return False
    
    def set_position(self, position: int) -> bool:
        """
        Set the position of the servo motor.
        
        Args:
            position: Target position (0-4095, where 0-4095 represents 0-360 degrees)
            
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        if position < 0 or position > 4095:
            logger.error(f"Invalid position: {position}. Must be between 0 and 4095.")
            return False
        
        logger.info(f"Setting motor ID {self.motor_id} to position {position}")
        
        position_bytes = position.to_bytes(2, byteorder='little')
        
        response = self._send_command(self.CMD_SET_POSITION, position_bytes)
        
        if response:
            self.current_position = position
            logger.info(f"Successfully set motor ID {self.motor_id} to position {position}")
            return True
        else:
            logger.error(f"Failed to set motor ID {self.motor_id} to position {position}")
            return False
    
    def set_speed(self, speed: int) -> bool:
        """
        Set the rotation speed of the servo motor.
        
        Args:
            speed: Target speed (0-1023)
            
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        if speed < 0 or speed > 1023:
            logger.error(f"Invalid speed: {speed}. Must be between 0 and 1023.")
            return False
        
        logger.info(f"Setting motor ID {self.motor_id} to speed {speed}")
        
        speed_bytes = speed.to_bytes(2, byteorder='little')
        
        response = self._send_command(self.CMD_SET_SPEED, speed_bytes)
        
        if response:
            self.current_speed = speed
            logger.info(f"Successfully set motor ID {self.motor_id} to speed {speed}")
            return True
        else:
            logger.error(f"Failed to set motor ID {self.motor_id} to speed {speed}")
            return False
    
    def get_position(self) -> Optional[int]:
        """
        Get the current position of the servo motor.
        
        Returns:
            Optional[int]: The current position of the servo or None if failed
        """
        logger.info(f"Reading position of motor ID {self.motor_id}")
        
        response = self._send_command(self.CMD_READ_POSITION)
        
        if response and len(response) >= 6:
            position = response[4] + (response[5] << 8)
            self.current_position = position
            logger.info(f"Motor ID {self.motor_id} position: {position}")
            return position
        else:
            logger.error(f"Failed to read position of motor ID {self.motor_id}")
            return None
    
    def get_speed(self) -> Optional[int]:
        """
        Get the current speed of the servo motor.
        
        Returns:
            Optional[int]: The current speed of the servo or None if failed
        """
        logger.info(f"Reading speed of motor ID {self.motor_id}")
        
        response = self._send_command(self.CMD_READ_SPEED)
        
        if response and len(response) >= 6:
            speed = response[4] + (response[5] << 8)
            self.current_speed = speed
            logger.info(f"Motor ID {self.motor_id} speed: {speed}")
            return speed
        else:
            logger.error(f"Failed to read speed of motor ID {self.motor_id}")
            return None
    
    def stop(self) -> bool:
        """
        Stop the servo motor.
        
        Returns:
            bool: True if command was sent successfully, False otherwise
        """
        logger.info(f"Stopping motor ID {self.motor_id}")
        
        response = self._send_command(self.CMD_STOP)
        
        if response:
            logger.info(f"Successfully stopped motor ID {self.motor_id}")
            return True
        else:
            logger.error(f"Failed to stop motor ID {self.motor_id}")
            return False


class MotorController:
    """
    Controller for multiple STS3215 motors.
    """
    
    def __init__(self, port: str = '/dev/ttyACM0', baudrate: int = 115200):
        """
        Initialize the motor controller.
        
        Args:
            port: The serial port to use for communication
            baudrate: The baudrate for serial communication
        """
        self.port = port
        self.baudrate = baudrate
        self.motors: List[STS3215Motor] = []
        
    def add_motor(self, motor_id: int) -> STS3215Motor:
        """
        Add a motor to the controller.
        
        Args:
            motor_id: The ID of the motor
            
        Returns:
            STS3215Motor: The created motor object
        """
        motor = STS3215Motor(motor_id, self.port, self.baudrate)
        self.motors.append(motor)
        return motor
    
    def connect_all(self) -> bool:
        """
        Connect to all motors.
        
        Returns:
            bool: True if all connections successful, False otherwise
        """
        success = True
        for motor in self.motors:
            if not motor.connect():
                success = False
        return success
    
    def disconnect_all(self) -> None:
        """Disconnect from all motors."""
        for motor in self.motors:
            motor.disconnect()
    
    def stop_all(self) -> None:
        """Stop all motors."""
        for motor in self.motors:
            motor.stop()
