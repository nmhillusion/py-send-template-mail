from PyQt6.QtWidgets import QFileDialog

from gui.component import logging_emitter
from gui.stage import IMainStage
from service import parse_data_file_to_send_items


class MainStageController:
    def __init__(self, main_window_: IMainStage):
        self.main_window_ = main_window_

    def open_chose_data_file_dialog(self):
        data_file_name_, _ = QFileDialog.getOpenFileName(self.main_window_, 'Open file',
                                                         '/', "Excel file (*.xls *.xlsx)")
        logging_emitter.info(f"chosen data file path: {data_file_name_}")
        return data_file_name_

    def send_all(self):
        logging_emitter.info("send all mails")

    def __get_headers_of_send_items(self, send_items_: list[dict[str, str]]) -> list[str]:
        headers_: list[str] = []

        if send_items_ is not None:
            if 0 < len(send_items_):
                first_item_ = send_items_[0]
                keys_ = first_item_.keys()
                for k_ in keys_:
                    headers_.append(k_)

        return headers_

    def load_data(self, data_file_name_: str):
        if (data_file_name_ is None):
            logging_emitter.warning("data file is empty")
            return

        logging_emitter.info(f"chosen data file from {data_file_name_}")

        send_items_: list[dict[str, str]] = parse_data_file_to_send_items(data_file_name_)
        headers_: list[str] = self.__get_headers_of_send_items(send_items_)

        self.main_window_.dataList.setAlternatingRowColors(True)
        self.main_window_.dataList.setColumnCount(len(headers_))
        self.main_window_.dataList.setRowCount(len(send_items_))

        self.main_window_.dataList.setHorizontalHeaderLabels(headers_)
        # self.main_window_.dataList.setItem(0, 0, QTableWidgetItem("a"))
        # self.main_window_.dataList.setItem(0, 1, QTableWidgetItem("1 a"))
