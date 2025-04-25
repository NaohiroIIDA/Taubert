# Taubert

Taubert is a Python-based control system for an omnidirectional robot using a Raspberry Pi and three Freetech STS3215 servo motors with omni-wheels positioned at 120-degree intervals.

## Features

- Control of Freetech STS3215 servo motors via serial communication
- Omnidirectional movement using three omni-wheels
- Simple API for robot control
- Command-line interface for basic operations

## Hardware Requirements

- Raspberry Pi (3 or 4 recommended)
- 3x Freetech STS3215 servo motors
- 3x Omni-wheels
- Power supply for the Raspberry Pi and servo motors
- Appropriate mechanical chassis with the motors positioned at 120-degree intervals

## Installation

### On the Raspberry Pi

1. Clone this repository:
   ```
   git clone https://github.com/NaohiroIIDA/Taubert.git
   cd Taubert
   ```

2. Install the package and dependencies:
   ```
   pip install -e .
   ```

## Usage

### Basic Movement Control

```python
from taubert.main import TaubertRobot

# Create the robot instance
robot = TaubertRobot()

# Connect to the hardware
if robot.connect():
    try:
        # Move forward
        robot.omni_drive.move_forward(0.5)  # 0.5 is the speed (0.0 to 1.0)
        
        # Move in a specific direction
        robot.omni_drive.move(vx=0.3, vy=0.4, omega=0.0)  # x, y velocities and rotation
        
        # Rotate
        robot.omni_drive.rotate_clockwise(0.3)
        
    finally:
        # Always stop and disconnect when done
        robot.stop()
        robot.disconnect()
```

### Command Line Interface

The package provides a command-line interface for basic operations:

```
# Run a movement demonstration
taubert --demo

# Specify custom servo IDs and serial port
taubert --servo-ids 1 2 3 --port /dev/ttyAMA0 --baudrate 115200
```

## Development

### Project Structure

- `src/taubert/motor/`: Servo motor control
- `src/taubert/movement/`: Omnidirectional movement control
- `src/taubert/main.py`: Main robot control class and CLI
- `examples/`: Example scripts

### Running Examples

```
python examples/basic_movement.py
```

## License

MIT

## Author

Naohiro IIDA (nao@nekotorobot.com)
