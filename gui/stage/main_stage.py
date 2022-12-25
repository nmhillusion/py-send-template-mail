__all__ = ["MainWindow"]

from os import path

from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QTextEdit, QTableWidget

from gui.component import logging_emitter
from gui.controller import MainStageController
from gui.stage import IMainStage


class MainWindow(QMainWindow, IMainStage):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon(path.dirname(__file__) + "/../resource/app_icon.png"))

        self.main_stage_controller_ = MainStageController(self)

        self.data_file_name_: str | None = None
        ui_ = uic.loadUi(path.dirname(__file__) + "/../resource/main_stage.ui", self)
        logging_emitter.apply_widget(ui_.logList)

        self.inp_data_file_path_: QTextEdit = ui_.inpDataFilePath
        self.btn_browse: QPushButton = ui_.btnBrowse
        self.btn_browse.pressed.connect(self.open_chose_data_file_dialog)

        self.btn_load_data_: QPushButton = ui_.btnLoadData
        self.btn_load_data_.pressed.connect(lambda: self.main_stage_controller_.load_data(self.data_file_name_))

        self.btn_send_all_: QPushButton = ui_.btnSendAll
        self.btn_send_all_.pressed.connect(lambda: self.main_stage_controller_.send_all(self.data_file_name_))

        self.dataList: QTableWidget = ui_.dataList

    def open_chose_data_file_dialog(self):
        data_file_name_ = self.main_stage_controller_.open_chose_data_file_dialog()
        self.data_file_name_ = data_file_name_
        self.inp_data_file_path_.setPlainText(data_file_name_)

        enable_action_ = data_file_name_ is not None
        self.btn_load_data_.setEnabled(enable_action_)
        self.btn_load_data_.setEnabled(enable_action_)
