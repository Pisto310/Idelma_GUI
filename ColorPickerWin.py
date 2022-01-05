from PyQt5.QtWidgets import *

app = QApplication([])
button = QPushButton('Click')

def on_button_clicked():
    msg = QMessageBox()
    msg.setStandardButtons(QMessageBox.Close)
    msg.setIcon(QMessageBox.Information)
    msg.setText("This is a message box")
    msg.setInformativeText("This is additional information")
    msg.setWindowTitle("MessageBox demo")
    msg.setDetailedText("The details are as follows:")
    msg.exec()

button.clicked.connect(on_button_clicked)
button.show()
app.exec()