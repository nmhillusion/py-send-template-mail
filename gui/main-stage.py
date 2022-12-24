import logging
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, QFileDialog


class OMainWindow(QMainWindow):
    def __init__(self):
        super(OMainWindow, self).__init__()

        self.data_file_name_: str | None = None
        ui_ = uic.loadUi("resource/main_stage.ui", self)

        self.inp_data_file_path_: QTextEdit = ui_.inpDataFilePath
        self.btn_browse: QPushButton = ui_.btnBrowse
        self.btn_browse.pressed.connect(self.open_chose_data_file_dialog)

        btn_load_data_: QPushButton = ui_.btnLoadData
        btn_load_data_.pressed.connect(self.load_data)

        btn_send_all_: QPushButton = ui_.btnSendAll
        btn_send_all_.pressed.connect(self.send_all)

        self.dataList: QTableWidget = ui_.dataList
        self.size()

    def open_chose_data_file_dialog(self):
        data_file_name_, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                                         '/', "Excel file (*.xls *.xlsx)")
        print("will load data from path: ", data_file_name_)
        self.data_file_name_ = data_file_name_
        self.inp_data_file_path_.setPlainText(data_file_name_)

    def send_all(self):
        print("send all mails")

    def load_data(self):
        if (self.data_file_name_ is None):
            logging.warning("data file is empty")
            return

        print("chosen data file from ", self.data_file_name_)

        self.dataList.setRowCount(3)
        self.dataList.setColumnCount(2)
        self.dataList.setHorizontalHeaderLabels(["Id", "Name"])
        self.dataList.setItem(0, 0, QTableWidgetItem("a"))
        self.dataList.setItem(0, 1, QTableWidgetItem("1 a"))

        self.dataList.setItem(1, 0, QTableWidgetItem("b"))
        self.dataList.setItem(1, 1, QTableWidgetItem("2 b"))

        self.dataList.setItem(2, 0, QTableWidgetItem("c"))
        self.dataList.setItem(2, 1, QTableWidgetItem("3 c"))


app = QApplication(sys.argv)
main_window_ = OMainWindow()
main_window_.show()
sys.exit(app.exec())
