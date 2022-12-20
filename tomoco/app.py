import sys

import json
import zmq

from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

class App(QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setWindowTitle('Tomoco: Tomography Data Acquisition')
        self.button = QPushButton('Go!')
        layout = QVBoxLayout()
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

    def buttonPressed(self):
        # Currently being a little lame - only update state on start/stop.
        print('Button pressed!', self.button.text())
        if self.button.text() == 'Go':
            self.button.setText('Stop')
        else:
            self.button.setText('Go')
        
        self.run("scan", "([det], motor, 1, 5, 5)", "{}")

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