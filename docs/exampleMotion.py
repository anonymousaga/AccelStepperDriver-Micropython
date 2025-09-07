import AccelStepperMotion

stepper = AccelStepperMotion.StepperMotion(14) # STEP Pin on GPIO14

stepper.set_params(accel=2, speed=100, steps_per_unit=90) # 90 steps per centimeter

stepper.move(50, speed=40, accel=6)
stepper.move(100) # uses the initially defined parameters for accel/speed from line 5
