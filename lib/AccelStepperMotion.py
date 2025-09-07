from machine import Pin
from time import sleep_us
from math import sqrt

class StepperMotion:
    """A stepper motor driver with acceleration control.
    
    Provides smooth acceleration and deceleration profiles for stepper motor control.
    """
    
    def __init__(self, step_pin):
        """Initialize stepper driver.
        
        Args:
            step_pin (int): GPIO pin number for step control
            steps_per_unit (float): Number of steps per unit of movement
        """
        self.step_pin = Pin(step_pin, Pin.OUT)
        
        # Parameters
        self.acceleration = 5
        self.speed = 100
        self.steps_per_unit = 50
        
        # Derived constants
        self.CALCS_CONSTANT = 1020000/self.steps_per_unit

    def _calc_step_delay(self, speed1):
        """Calculate step delay in microseconds for given speed."""
        if speed1 <= 0:
            raise ValueError("Speed must be greater than 0")
        return int(self.CALCS_CONSTANT / speed1) - 10
    
    def _calc_accel_delay(self, step_num, accel1):
        """Calculate delay during acceleration/deceleration."""
        return self._calc_step_delay(0.3 * accel1 * sqrt(step_num + 2))
        
    def move(self, distance, speed=None, accel=None):
        """Move stepper motor by specified number of steps.
        
        Args:
            distance (float): Number of units to move
            speed (float, optional): Speed override in units/sec
            accel (float, optional): Acceleration override
        """
        if speed is None:
            speed = self.speed
        if accel is None:
            accel = self.acceleration
            
        steps = abs(int(distance * self.steps_per_unit))
        if steps == 0:
            return
            
        # Calculate acceleration profile
        target_delay = self._calc_step_delay(speed)
        accel_steps = int(steps * 0.496)
        
        # Calculate acceleration delays
        delays = []
        for i in range(1, accel_steps):
            delay = self._calc_accel_delay(i, accel)
            if delay <= target_delay:
                accel_steps = i
                break
            delays.append(delay)

        # Ensure target delay is not less than minimum delay
        target_delay = delay
        
        # Pre-calculate ranges
        accel_range = range(1, accel_steps - 1)
        cruise_range = range(accel_steps - 1, 2 + steps - accel_steps)
        decel_range = range((-accel_steps) + 2, 0)
        
        # Execute movement
        for i in accel_range:
            self.step_pin.value(1)
            self.step_pin.value(0)
            sleep_us(delays[i])
            
        for _ in cruise_range:
            self.step_pin.value(1)
            self.step_pin.value(0)
            sleep_us(target_delay)
            
        for i in decel_range:
            self.step_pin.value(1)
            self.step_pin.value(0)
            sleep_us(delays[-i])
            
    def set_params(self, accel=None, speed=None, steps_per_unit=None):
        """Update driver parameters.
        
        Args:
            accel (float, optional): New acceleration value
            speed (float, optional): New speed value
            steps_per_unit (float, optional): New steps per unit
        """
        if accel is not None:
            self.acceleration = accel
        if speed is not None:
            self.speed = speed
        if steps_per_unit is not None:
            self.steps_per_unit = steps_per_unit
            self.CALCS_CONSTANT = 1020000/self.steps_per_unit

