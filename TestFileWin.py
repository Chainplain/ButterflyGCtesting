from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import  QtGui

class FileSelectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a File Dialog
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle("Select File")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setViewMode(QFileDialog.Detail)
        # file_dialog.setOptions(QFileDialog.DontUseNativeDialog)

        # Show the File Dialog and get the selected file(s)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            for file in selected_files:
                print("Selected File:", file)
            

if __name__ == "__main__":
    app = QApplication([])
    window = FileSelectionWindow()
    window.show()
    QtGui.QGuiApplication.instance().exec_()