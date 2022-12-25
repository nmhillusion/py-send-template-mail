import traceback
from functools import partial

from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem, QPushButton

from gui.component import logging_emitter
from gui.stage import IMainStage
from service import parse_data_file_to_send_items
from service.main_runner import preview_send_item, send_all_items


class MainStageController:
    def __init__(self, main_window_: IMainStage):
        self.main_window_ = main_window_

    def open_chose_data_file_dialog(self):
        data_file_name_, _ = QFileDialog.getOpenFileName(self.main_window_, 'Open file',
                                                         '/', "Excel file (*.xls *.xlsx)")
        logging_emitter.info(f"chosen data file path: {data_file_name_}")
        return data_file_name_

    def send_all(self, data_file_name_: str):
        logging_emitter.info("send all mails")
        if (data_file_name_ is None):
            logging_emitter.error("data file is empty")
            return
        try:
            send_all_items(data_excel_path_=self.main_window_.data_file_name_)
        except Exception as ex:
            traceback.print_exc()
            logging_emitter.error(str(ex))

    def __get_headers_of_send_items(self, send_items_: list[dict[str, str]]) -> list[str]:
        headers_: list[str] = []

        if send_items_ is not None:
            if 0 < len(send_items_):
                first_item_ = send_items_[0]
                keys_ = first_item_.keys()
                for k_ in keys_:
                    headers_.append(k_)
        headers_.append("Action")

        return headers_

    def load_data(self, data_file_name_: str):
        if (data_file_name_ is None):
            logging_emitter.error("data file is empty")
            return

        logging_emitter.info(f"chosen data file from {data_file_name_}")

        send_items_: list[dict[str, str]] = parse_data_file_to_send_items(data_file_name_)
        headers_: list[str] = self.__get_headers_of_send_items(send_items_)

        self.main_window_.dataList.setAlternatingRowColors(True)
        self.main_window_.dataList.colorCount()
        self.main_window_.dataList.setWordWrap(True)
        self.main_window_.dataList.setColumnCount(len(headers_))
        self.main_window_.dataList.setRowCount(len(send_items_))

        self.main_window_.dataList.setHorizontalHeaderLabels(headers_)

        for row_idx_, si_ in enumerate(send_items_):
            for col_idx_ in range(len(headers_) - 1):
                self.main_window_.dataList.setItem(row_idx_, col_idx_, QTableWidgetItem(si_[headers_[col_idx_]]))

            btn_preview_ = QPushButton("Preview")
            btn_preview_.pressed.connect(partial(self.preview_send_item, si_))
            self.main_window_.dataList.setCellWidget(row_idx_, len(headers_) - 1, btn_preview_)

    def preview_send_item(self, si_: dict[str, str]):
        try:
            preview_send_item(si_)
        except Exception as ex:
            traceback.print_exc()
            logging_emitter.error(str(ex))
