import sys

import json
import zmq

from qtpy.QtCore import (
    Signal,
    Slot,
    QObject,
)

from qtpy.QtWidgets import (
    QApplication,
    QCommonStyle,
    QStyle,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
)

from .motors import *

class App(QMainWindow):
    # Set up a few signals for the motor positions
    motorSignalZ = Signal(float)

    def __init__(self, parent: QObject = None) -> None:
        super(App, self).__init__(parent)
        self.setWindowTitle('Tomoco: Tomography Data Acquisition')

        self.zps = zps

        self.z = 1000.0

        layout = QVBoxLayout()

        # Cluster for motor controls
        style = QCommonStyle()
        gridLayout = QGridLayout()
        self.leftButton = QPushButton(style.standardIcon(QStyle.SP_ArrowLeft), '')
        self.rightButton = QPushButton(style.standardIcon(QStyle.SP_ArrowRight), '')
        self.upButton = QPushButton(style.standardIcon(QStyle.SP_ArrowUp), '')
        self.downButton = QPushButton(style.standardIcon(QStyle.SP_ArrowDown), '')
        gridLayout.addWidget(self.upButton, 0, 1)
        gridLayout.addWidget(self.downButton, 2, 1)
        gridLayout.addWidget(self.leftButton, 1, 0)
        gridLayout.addWidget(self.rightButton, 1, 2)
        layout.addLayout(gridLayout)
        layout.addStretch()

        self.upButton.clicked.connect(self.moveZUp)
        self.downButton.clicked.connect(self.moveZDown)

        self.labelZ = QLabel("Unknown")
        layout.addWidget(self.labelZ)

        self.button = QPushButton('Go!')
        hButtonBox = QHBoxLayout()
        hButtonBox.addStretch()
        hButtonBox.addWidget(self.button)
        hButtonBox.addStretch()
        layout.addLayout(hButtonBox)

        # Set main windows widget using our central layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Add button signal to slot to start/stop
        self.button.clicked.connect(self.buttonPressed)

        # Connect up a motor epics signal to a Qt slot...
        self.motorSignalZ.connect(self.updatePositionZ)
        self.zps.sz.subscribe(self.updateMotorZ)

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.connect('tcp://127.0.0.1:5556')

    def buttonPressed(self) -> None:
        # Currently being a little lame - only update state on start/stop.
        if self.button.text() == 'Go':
            self.button.setText('Stop')
        else:
            self.button.setText('Go')

        self.run("scan", "([det], motor, 1, 5, 5)", "{}")

    def updateMotorZ(self, value, old_value = None, timestamp = None, **kwargs) -> None:
        self.z = float(value)
        self.motorSignalZ.emit(float(value))

    @Slot()
    def moveZUp(self) -> None:
        self.zps.sz.set(self.z + 20)

    @Slot()
    def moveZDown(self) -> None:
        self.zps.sz.set(self.z - 20)

    @Slot(float)
    def updatePositionZ(self, value: float) -> None:
        self.labelZ.setText(f'z = {value:4.3f}')

    def run(self, plan_name, args, kwargs):
        to_send = json.dumps({"plan_name": plan_name, "plan_args": args, "plan_kwargs": kwargs}).encode()
        self.socket.send(to_send)
        print('sent', to_send)
        msg = self.socket.recv()
        if msg:
            decoded_msg = json.loads(msg.decode())
            print('received', decoded_msg)


def run():
    # Set up some application basics for saving settings
    QApplication.setOrganizationName('BNL')
    QApplication.setOrganizationDomain('bnl.gov')
    QApplication.setApplicationName('tomoco')

    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the form
    window = App()
    window.show()

    # Run the main Qt loop
    sys.exit(app.exec_())
