import sys
import hashlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QToolBar
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

class MyTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dragMoveEvent(self, event):
        event.accept()
        
    def dropEvent(self, event):
        file_path = []
        for url in event.mimeData().urls():
            file_path.append(url.toLocalFile())
        addFileHash(file_path, self)

def main():
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("SHA256 本機端計算工具")

    toolbar = QToolBar()
    window.addToolBar(toolbar)

    choose_button = QPushButton("Choose Files")
    delete_button = QPushButton('Delete All')

    toolbar.addWidget(choose_button)
    toolbar.addWidget(delete_button)

    table = MyTableWidget()
    table.setColumnCount(2)
    table.setHorizontalHeaderLabels(["File Name", "SHA-256"])

    central_widget = QWidget()
    central_layout = QVBoxLayout()
    central_layout.addWidget(table)
    central_widget.setLayout(central_layout)
    window.resize(800, 600)
    window.setCentralWidget(central_widget)
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    choose_button.clicked.connect(lambda: open_file_dialog(table))
    delete_button.clicked.connect(lambda: deleteAll(table))

    window.show()
    sys.exit(app.exec_())

def open_file_dialog(table):
    file_dialog = QFileDialog()
    selected_files, _ = file_dialog.getOpenFileNames()
    addFileHash(selected_files, table)
    

def addFileHash(selected_files, table):
    print(selected_files)
    row = table.rowCount()
    if selected_files:
        table.setRowCount(len(selected_files) + row)
        for i, file in enumerate(selected_files):
            file_info = QFileInfo(file)
            file_name = file_info.fileName()
            # file_size = file_info.size()
            # file_type = file_info.completeSuffix()
            table.setItem(i + row, 0, QTableWidgetItem(file_name))
            table.setItem(i + row, 1, QTableWidgetItem(computeHash(file)))
        for column in range(table.columnCount()):
            table.resizeColumnToContents(column)
        

def computeHash(file_path):
    BufferSize = 65536
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(BufferSize)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()

def deleteAll(table):
    table.setRowCount(0)

if __name__ == "__main__":
    main()