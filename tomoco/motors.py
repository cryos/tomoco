from ophyd import (
    EpicsMotor,
    EpicsSignal,
    EpicsSignalRO,
    Device,
    Component as Cpt,
)

# These classes are taken from the FXI profile and are just their EPICS motors.
class MyBaseMotor(EpicsMotor):
    dial_readback = Cpt(EpicsSignalRO, ".DRBV")
    dial_counts = Cpt(EpicsSignalRO, ".RRBV")
    motor_res = Cpt(EpicsSignalRO, ".MRES")
    encoder_res = Cpt(EpicsSignalRO, ".ERES")
    motor_stat = Cpt(EpicsSignalRO, ".STAT")
    motor_calib = Cpt(EpicsSignal, ".SET")
    low_limit = Cpt(EpicsSignal, ".LLM")
    high_limit = Cpt(EpicsSignal, ".HLM")
    step_size = Cpt(EpicsSignal, ".TWV")

class MyEpicsMotor(MyBaseMotor):
    def stop(self, success=False):
        self.user_setpoint.set(self.user_readback.get())
        Device.stop(self, success=success)

class TXMSampleStage(Device):
    sx = Cpt(MyEpicsMotor, "{Env:1-Ax:Xl}Mtr")
    sy = Cpt(MyEpicsMotor, "{Env:1-Ax:Yl}Mtr")
    sz = Cpt(MyEpicsMotor, "{Env:1-Ax:Zl}Mtr")
    pi_x = Cpt(MyBaseMotor, "{TXM:1-Ax:X}Mtr")
    pi_r = Cpt(MyEpicsMotor, "{TXM:1-Ax:R}Mtr")

zps = TXMSampleStage("XF:18IDB-OP", name="zps")
