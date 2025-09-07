# AccelStepperDriver-Micropython

Drive stepper motor drivers (A4988 &amp; compatibles) with acceleration.

## Installation
Load all files from [lib/](lib/) onto the MicroPython board.

## AccelStepperMotion

This controls ONLY the step pin. It uses speed and acceleration variables to pre-calculate a square root acceleration curve, optimal for high-torque applications. Creates a class `StepperMotion`.

### Example
Basic movement and parameter functionality: [exampleMotion.py](docs/exampleMotion.py)


### Methods

- `__init__(step_pin)`
  - Initializes stepper motor with given step pin
  - Parameters:
    - `step_pin` (int): Pin number for step control

- `move(distance, speed=None, accel=None)`
  - Moves the stepper motor by a specified distance (in units), with optional speed and acceleration overrides.
  - Parameters:
    - `distance` (float): Number of units to move (positive only)
    - `speed` (float, optional): Speed override in units/sec
    - `accel` (float, optional): Acceleration override

- `set_params(accel=None, speed=None, steps_per_unit=None)`
  - Updates driver parameters for acceleration, speed, and steps per unit.
  Parameters:
    - `accel` (float, optional): New acceleration value
    - `speed` (float, optional): New speed value
    - `steps_per_unit` (float, optional): New steps per unit
