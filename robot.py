from phoenix6 import configs, controls, hardware, signals
from wpilib import TimedRobot, Joystick, XboxController

class MyRobot(TimedRobot):
    def __init__(self, period = 0.02):
        super().__init__(period)
        self.xboxcontroller = XboxController(0)
        self.backMotor = hardware.TalonFX(0, "rio")
        
    def robotInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopPeriodic(self):
        self.backMotor.set(self.xboxcontroller.getRightTriggerAxis())
