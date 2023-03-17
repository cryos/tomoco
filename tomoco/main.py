import sys

from qtpy.QtWidgets import QApplication

from .mainwindow import MainWindow

def main():
    # Set up some application basics for saving settings
    QApplication.setOrganizationName('BNL')
    QApplication.setOrganizationDomain('bnl.gov')
    QApplication.setApplicationName('tomoco')

    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the form
    window = MainWindow()
    window.show()

    # Run the main Qt loop
    sys.exit(app.exec_())
