import json
import zmq

from qtpy.QtCore import (
    Signal,
    Slot,
    QObject,
)

from qtpy.QtWidgets import (
    QCommonStyle,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
)

if False:
    from .motors import *
else:
    from .motors_simulated import *
from .motor import Motor

from .motorwidget import MotorWidget

class MainWindow(QMainWindow):
    # Set up a few signals for the motor positions
    motorSignalZ = Signal(float)

    def __init__(self, parent: QObject = None) -> None:
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Tomoco: Tomography Data Acquisition')

        self.zps = zps

        self.motors = {}
        self.motors['x'] = Motor(zps.sx)
        self.motors['y'] = Motor(zps.sy)
        self.motors['z'] = Motor(zps.sz)
        self.motors['r'] = Motor(zps.pi_r)

        self.motorWidgets = {}
        self.motorWidgets['x'] = MotorWidget(self.motors['x'])
        self.motorWidgets['y'] = MotorWidget(self.motors['y'])
        self.motorWidgets['z'] = MotorWidget(self.motors['z'])
        self.motorWidgets['r'] = MotorWidget(self.motors['r'])
        self.motorWidget = self.motorWidgets['x']

        layout = QVBoxLayout()

        # Cluster for motor controls
        style = QCommonStyle()
        gridLayout = QGridLayout()
        gridLayout.addWidget(QLabel('<b>Variable</b>'), 0, 0)
        gridLayout.addWidget(QLabel('<b>Readout</b>'), 0, 1)
        gridLayout.addWidget(QLabel('<b>Limits</b>'), 0, 2)
        gridLayout.addWidget(QLabel('<b>Set</b>'), 0, 3)
        gridLayout.addWidget(QLabel('<b>Step</b>'), 0, 4)
        gridLayout.addWidget(QLabel('<b>x (\xB5m)</b>'), 1, 0)
        gridLayout.addWidget(QLabel('<b>y (\xB5m)</b>'), 2, 0)
        gridLayout.addWidget(QLabel('<b>z (\xB5m)</b>'), 3, 0)
        gridLayout.addWidget(QLabel('<b>r (\xB0)</b>'), 4, 0)
        gridLayout.addWidget(self.motorWidgets['x'].posLabel, 1, 1)
        gridLayout.addWidget(self.motorWidgets['x'].limitsLabel, 1, 2)
        gridLayout.addWidget(self.motorWidgets['x'].posSpinBox, 1, 3)
        gridLayout.addWidget(self.motorWidgets['x'].stepSpinBox, 1, 4)
        gridLayout.addWidget(self.motorWidgets['y'].posLabel, 2, 1)
        gridLayout.addWidget(self.motorWidgets['y'].limitsLabel, 2, 2)
        gridLayout.addWidget(self.motorWidgets['y'].posSpinBox, 2, 3)
        gridLayout.addWidget(self.motorWidgets['y'].stepSpinBox, 2, 4)
        gridLayout.addWidget(self.motorWidgets['z'].posLabel, 3, 1)
        gridLayout.addWidget(self.motorWidgets['z'].limitsLabel, 3, 2)
        gridLayout.addWidget(self.motorWidgets['z'].posSpinBox, 3, 3)
        gridLayout.addWidget(self.motorWidgets['z'].stepSpinBox, 3, 4)
        gridLayout.addWidget(self.motorWidgets['r'].posLabel, 4, 1)
        gridLayout.addWidget(self.motorWidgets['r'].limitsLabel, 4, 2)
        gridLayout.addWidget(self.motorWidgets['r'].posSpinBox, 4, 3)
        gridLayout.addWidget(self.motorWidgets['r'].stepSpinBox, 4, 4)
        layout.addLayout(gridLayout)
        layout.addStretch()

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

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.connect('tcp://127.0.0.1:5556')

    def buttonPressed(self) -> None:
        # Currently being a little lame - only update state on start/stop.
        if self.button.text() == 'Go':
            self.button.setText('Stop')
        else:
            self.button.setText('Go')

        self.run("mv", "(zps.pi_r, 0.0)", "{}")

    def run(self, plan_name, args, kwargs):
        to_send = json.dumps({"plan_name": plan_name, "plan_args": args, "plan_kwargs": kwargs}).encode()
        self.socket.send(to_send)
        print('sent', to_send)
        msg = self.socket.recv()
        if msg:
            decoded_msg = json.loads(msg.decode())
            print('received', decoded_msg)
