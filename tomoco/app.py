import sys

from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
)

class App(QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setWindowTitle("Tomoco: Tomography Data Acquisition")

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