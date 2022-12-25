from os import path

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, QFileDialog

from gui import logging_emitter


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.data_file_name_: str | None = None
        ui_ = uic.loadUi(path.dirname(__file__) + "/resource/main_stage.ui", self)
        logging_emitter.apply_widget(ui_.logList)

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
        logging_emitter.info(f"will load data from path: {data_file_name_}")
        self.data_file_name_ = data_file_name_
        self.inp_data_file_path_.setPlainText(data_file_name_)

    def send_all(self):
        logging_emitter.info("send all mails")

    def load_data(self):
        if (self.data_file_name_ is None):
            logging_emitter.warning("data file is empty")
            return

        logging_emitter.info(f"chosen data file from {self.data_file_name_}")

        self.dataList.setRowCount(3)
        self.dataList.setColumnCount(2)
        self.dataList.setHorizontalHeaderLabels(["Id", "Name"])
        self.dataList.setItem(0, 0, QTableWidgetItem("a"))
        self.dataList.setItem(0, 1, QTableWidgetItem("1 a"))

        self.dataList.setItem(1, 0, QTableWidgetItem("b"))
        self.dataList.setItem(1, 1, QTableWidgetItem("2 b"))

        self.dataList.setItem(2, 0, QTableWidgetItem("c"))
        self.dataList.setItem(2, 1, QTableWidgetItem("3 c"))
