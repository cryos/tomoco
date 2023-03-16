from ophyd.sim import motor, motor1, motor2, motor3

# Stupidly simple simulated motors for testing/development.
class TXMSampleStage():
    sx = motor1
    sy = motor2
    sz = motor3
    pi_x = motor
    pi_r = motor

zps = TXMSampleStage()
