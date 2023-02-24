from qtpy.QtCore import (
    Signal,
    Slot,
    QObject,
)

from ophyd import (
    EpicsMotor,
)

""" A QObject derived class for Ophyd motor objects that fires signals. """
class Motor(QObject):
    motorMoved = Signal(float)

    def __init__(self, motor: EpicsMotor, parent: QObject = None) -> None:
        super(Motor, self).__init__(parent)
        self.pos = 0.0
        self.motor = motor
        self.motor.subscribe(self.updateMotor)

    def updateMotor(self, value, old_value = None, timestamp = None, **kwargs) -> None:
        self.pos = float(value)
        self.motorMoved.emit(float(value))

    @Slot(float)
    def setPosition(self, pos: float) -> None:
        self.motor.set(pos)
