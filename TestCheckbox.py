from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QCheckBox, QWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a checkbox
        self.checkbox = QCheckBox("Check me")
        self.checkbox.setChecked(True)  # Set the initial state of the checkbox

        # Connect the checkbox state changed signal to a slot
        self.checkbox.stateChanged.connect(self.checkbox_state_changed)

        # Set the checkbox as the central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.checkbox)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def checkbox_state_changed(self, state):
        if state == 0:
            print("Checkbox is unchecked")
        else:
            print("Checkbox is checked")

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()