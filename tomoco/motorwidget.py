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

        self._posValid = False
        self.pos = motor.pos
        self.step = 20.0
        self.range = [-9999, 9999]

        # Connect up our class to the motor signal.
        self.motor = motor
        self.motor.motorMoved.connect(self.motorMoved)

        # Lazily initialize and connect up components as and when they are used.
        self._incButton = None
        self._decButton = None
        self._posLineEdit = None
        self._posSpinBox = None
        self._stepSpinBox = None
        self._posLabel = None
        self._stepLineEdit = None
        self._limitsLabel = None

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
            self._posSpinBox.setMinimum(self.range[0])
            self._posSpinBox.setMaximum(self.range[1])
            self._posSpinBox.setValue(self.pos)
            self._posSpinBox.setSingleStep(self.step)
            self._posSpinBox.setDecimals(3)
            self._posSpinBox.valueChanged.connect(self.posChanged)

        return self._posSpinBox

    @property
    def stepSpinBox(self) -> QWidget:
        if self._stepSpinBox is None:
            self._stepSpinBox = QDoubleSpinBox()
            self._stepSpinBox.setMinimum(0)
            self._stepSpinBox.setMaximum(1000)
            self._stepSpinBox.setDecimals(3)
            try:
                step = self.motor.motor.step_size.get()
            except AttributeError:
                step = 20
            self._stepSpinBox.setValue(step)
            self.stepChanged(step)
            self._stepSpinBox.valueChanged.connect(self.stepChanged)

        return self._stepSpinBox

    @property
    def posLabel(self) -> QWidget:
        if self._posLabel is None:
            self._posLabel = QLabel(self.posStr)

        return self._posLabel

    @property
    def limitsLabel(self) -> QWidget:
        if self._limitsLabel is None:
            self._limitsLabel = QLabel("Undef, Undef")
            try:
                low = self.motor.motor.low_limit.get()
            except AttributeError:
                low = -1000
            try:
                high = self.motor.motor.high_limit.get()
            except AttributeError:
                high = 1000
            self.range = [low, high]
            self._limitsLabel.setText(f'({low:4.3f}, {high:4.3f})')
            if self._posSpinBox:
                self._posSpinBox.setMinimum(low)
                self._posSpinBox.setMaximum(high)

        return self._limitsLabel

    @Slot(float)
    def motorMoved(self, pos: float) -> None:
        # Check which widgets are initialized that should be updated.
        self.pos = pos
        if not self._posValid:
            # The widgets were initialized before the first real position.
            self._posValid = True
            if self._posSpinBox:
                self._posSpinBox.blockSignals(True)
                self._posSpinBox.setValue(self.pos)
                self._posSpinBox.blockSignals(False)

        if self._posLabel:
            self._posLabel.setText(self.posStr)

    @Slot(float)
    def stepChanged(self, step: float) -> None:
        print ('step', step)
        self.step = step
        if self._posSpinBox:
            self._posSpinBox.setSingleStep(step)

    @Slot(float)
    def posChanged(self, pos: float) -> None:
        print ('moving to:', pos)

        self.motor.setPosition(pos)
