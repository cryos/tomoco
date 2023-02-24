from qtpy.QtCore import (
    Signal,
    Slot,
    QObject,
)

from qtpy.QtWidgets import (
    QCommonStyle,
    QStyle,
    QLabel,
    QPushButton,
    QLineEdit,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
)

from .motor import Motor

""" A factory class to coordinate motor control and feedback. """
class MotorWidget(QObject):
    def __init__(self, motor: Motor, parent: QObject = None) -> None:
        super(MotorWidget, self).__init__(parent)

        # Raise an error is the motor object is not valid.
        if motor is None:
            raise TypeError

        self.pos = 0.0
        self.step = 20.0

        # Connect up our class to the motor signal.
        self.motor = motor
        self.motor.motorMoved.connect(self.motorMoved)

        # Lazily initialize and connect up components as and when they are used.
        self._incButton = None
        self._decButton = None
        self._posLineEdit = None
        self._posSpinBox = None
        self._posLabel = None
        self._stepLineEdit = None

    @property
    def posStr(self) -> str:
        return f'{self.pos:4.3f}'
    
    @property
    def incButton(self) -> QWidget:
        style = QCommonStyle()
        if self._incButton is None:
            self._incButton = \
                QPushButton(style.standardIcon(QStyle.SP_ArrowRight), '')
            self._incButton.setToolTip("Increase")

        return self._incButton

    @property
    def decButton(self) -> QWidget:
        style = QCommonStyle()
        if self._decButton is None:
            self._decButton = \
                QPushButton(style.standardIcon(QStyle.SP_ArrowLeft), '')
            self._incButton.setToolTip("Decrease")

        return self._incButton

    @property
    def posLineEdit(self) -> QWidget:
        if self._posLineEdit is None:
            self._posLineEdit = QLineEdit("Unknown")

        return self._posLineEdit
    
    @property
    def posSpinBox(self) -> QWidget:
        if self._posSpinBox is None:
            self._posSpinBox = QDoubleSpinBox()
            self._posSpinBox.setValue(self.pos)
            self._posSpinBox.setSingleStep(self.step)
            self._posSpinBox.setDecimals(3)

        return self._posSpinBox

    @property
    def posLabel(self) -> QWidget:
        if self._posLabel is None:
            self._posLabel = QLabel("Unknown")

        return self._posLabel

    @Slot(float)
    def motorMoved(self, pos: float) -> None:
        # Check which widgets are initialized that should be updated.
        self.pos = pos
        if self._posLabel:
            self._posLabel.setText(self.posStr)
