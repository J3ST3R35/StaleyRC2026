from enum import Enum

from commands2 import Subsystem
from wpilib import RobotState
from ntcore.util import ntproperty

from wpimath.units import degrees

from phoenix6.hardware import TalonFX
from phoenix6.configs import TalonFXConfiguration, MotorOutputConfigs
from phoenix6.signals import InvertedValue, NeutralModeValue
from phoenix6.controls import PositionVoltage

from util.FalconLogger import FalconLogger

class Intake(Subsystem):
    class IntakeSpeeds:
        STOP = 0
        IN = ntproperty("/Settings/Intake/IntakeSpeed", defaultValue=0.8, persistent=True)

    class IntakePositions:
        '''
        Position setpoints for the intake in degrees
        0 is (should be) the horizontal/outward/deployed position
        90 is (should be) straight up
        '''
        MAX:degrees = 80 #NOTE: currently underestimate for safety in testing
        MIN:degrees = 10 #NOTE: currently underestimate for safety in testing

        IN:degrees = 80 #NOTE: currently underestimate for safety in testing
        OUT:degrees = 10 #NOTE: currently underestimate for safety in testing


    # Variable Declaration

    def __init__(self, intakeMotorID:int, pivotLeadMotorID:int, pivotFollowMotorID:int) -> None:
        ### Motor Setup
        ## Launch Motor
        self.intake_motor = TalonFX(intakeMotorID, "rio")

        #TODO: configs
        # m_config = TalonFXConfiguration()
        # self.launchMotor.configurator.apply(m_config)

        ## Pivot Motors
        #TODO: Pivot
        self.lead_pivot_motor = TalonFX(pivotLeadMotorID, "rio")
        # self.follow_pivot_motor = TalonFX(pivotFollowMotorID, "rio")

        # Config
        base_config = TalonFXConfiguration()
        base_config = base_config.with_motor_output(
            MotorOutputConfigs()
            .with_neutral_mode(NeutralModeValue.COAST)
        )

        self.lead_pivot_motor.configurator.apply(base_config)

        # follow_config = base_config.__setattr__
        
        # self.follow_pivot_motor.configurator.apply(base_config)

        ### Functionality Setup
        self.intake_speed = self.IntakeSpeeds.STOP
        self.pivot_setpoint = self.IntakePositions.IN

    def periodic(self) -> None:
        # Logging: Write Current Measured Subsystem State
        FalconLogger.logInput("/Intake/Inputs/launchMotor/velocity", self.intake_motor.get_velocity())

        # Run Subsystem: Set New State To Subsystem
        if RobotState.isDisabled():
            self.stop()
        else:
            self.run()
        
        # Logging: Write Post Operation Information
        FalconLogger.logOutput("/Intake/Outputs/Setpoint", self.getSetpoint())

    def run(self) -> None:
        ## Intake
        #control speed by percentage
        self.intake_motor.set(self.intake_speed)

        ## Pivot
        #control position
        self.lead_pivot_motor.set_control(PositionVoltage(self.pivot_setpoint))

    def stop(self) -> None:
        pass

    def setIntakeSpeed(self, speed:IntakeSpeeds) -> None:
        self.intake_speed = speed

    def getIntakeSpeed(self) -> IntakeSpeeds:
        return self.intake_speed
    
    def setPivotSetpoint(self, setpoint:IntakePositions|degrees) -> None:
        self.pivot_setpoint = setpoint
    
    def getPivotSetpoint(self) -> degrees:
        return self.pivot_setpoint