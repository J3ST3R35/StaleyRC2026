from phoenix6 import configs, controls, hardware, signals
from wpilib import TimedRobot, Joystick, XboxController

class MyRobot(TimedRobot):
    def __init__(self, period = 0.02):
        super().__init__(period)
        self.xboxcontroller = XboxController(0)
        self.iMotor = hardware.TalonFX(0, "rio")
        
    def robotInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopPeriodic(self):
        trigger = self.xboxcontroller.getRightTriggerAxis()
        power = trigger * 0.5
        self.iMotor.set(power)
        
