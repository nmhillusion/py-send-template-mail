import traceback
from functools import partial
from os import path
from typing import Callable

from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem, QPushButton, QMessageBox

from gui.component import logging_emitter
from gui.stage import IMainStage
from gui.state import StateService
from service import parse_data_file_to_send_items, read_setting
from service.main_runner import preview_send_item, send_all_items
from util import StringUtil, os_util
from util.mapping_util import mapping_config_to_func


class MainStageController:
    __KEY__prev_data_file_path = "prev.data.file.path"
    __KEY__prev_template_file_path = "prev.template.file.path"

    def __init__(self, main_window_: IMainStage):
        self.main_window_ = main_window_
        self.state_service_ = StateService()
        self.settings_ = read_setting()
        self.__load_converters()

    def load_previous_state(self):
        pre_data_file_path_ = self.state_service_.get_state(self.__KEY__prev_data_file_path)
        pre_template_file_path_ = self.state_service_.get_state(self.__KEY__prev_template_file_path)

        self.main_window_.data_file_name_ = pre_data_file_path_
        self.main_window_.template_file_name_ = pre_template_file_path_

        self.main_window_.re_enable_action_buttons()

    def save_state(self):
        state_ = {
            self.__KEY__prev_data_file_path: self.main_window_.data_file_name_,
            self.__KEY__prev_template_file_path: self.main_window_.template_file_name_
        }

        for key_ in state_:
            if not StringUtil.is_blank(state_[key_]):
                self.state_service_.save_state({
                    key_: state_[key_]
                })

    def __load_converters(self):
        self.converters_: dict[str, Callable] = mapping_config_to_func(self.settings_["converters"])

    def open_choose_data_file_dialog(self):
        prev_file_path_ = self.state_service_.get_state(self.__KEY__prev_data_file_path)
        start_path_ = path.dirname(prev_file_path_) if prev_file_path_ is not None else ""

        chosen_file_name_, _ = QFileDialog.getOpenFileName(self.main_window_
                                                           , "Open data file"
                                                           , start_path_
                                                           , "Excel file (*.xls *.xlsx)")
        logging_emitter.info(f"chosen data file path: {chosen_file_name_}")

        return chosen_file_name_

    def open_choose_template_file_dialog(self):
        prev_file_path_ = self.state_service_.get_state(self.__KEY__prev_template_file_path)
        start_path_ = path.dirname(prev_file_path_) if prev_file_path_ is not None else ""
        chosen_file_name_, _ = QFileDialog.getOpenFileName(self.main_window_
                                                           , "Open template file"
                                                           , start_path_
                                                           , "Template mail file (*.oft *.msg);;HTML file (*.html)")
        logging_emitter.info(f"chosen template file path: {chosen_file_name_}")

        return chosen_file_name_

    def send_all(self, data_file_name_: str):
        msg_box_ = QMessageBox()
        msg_box_.setIcon(QMessageBox.Icon.Information)
        msg_box_.setWindowTitle("Confirm")
        msg_box_.setText("Confirm to send all items?")
        msg_box_.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        return_value_ = msg_box_.exec()

        if QMessageBox.StandardButton.Ok != return_value_:
            logging_emitter.warning("cancelled to send all items request!")
            return

        logging_emitter.info("send all mails")
        if StringUtil.is_blank(data_file_name_):
            logging_emitter.error("data file is empty")
            return

        try:
            if StringUtil.is_blank(self.main_window_.template_file_name_):
                raise IOError("template_file_name_ is None")
            send_all_items(template_file_path_=self.main_window_.template_file_name_,
                           data_excel_path_=self.main_window_.data_file_name_,
                           converters_=self.converters_)
        except Exception as ex:
            traceback.print_exc()
            logging_emitter.error(str(ex))

    def __get_headers_of_send_items(self, send_items_: list[dict[str, str]]) -> list[str]:
        headers_: list[str] = ["Action"]

        if send_items_ is not None:
            if 0 < len(send_items_):
                first_item_ = send_items_[0]
                keys_ = first_item_.keys()
                for k_ in keys_:
                    headers_.append(k_)

        return headers_

    def load_data(self, data_file_name_: str):
        if StringUtil.is_blank(data_file_name_):
            logging_emitter.error("data file is empty")
            return

        logging_emitter.info(f"chosen data file from {data_file_name_}")

        send_items_: list[dict[str, str]] = parse_data_file_to_send_items(data_file_name_, converters_=self.converters_)
        headers_: list[str] = self.__get_headers_of_send_items(send_items_)

        self.main_window_.dataList.clear()
        self.main_window_.dataList.setAlternatingRowColors(True)
        self.main_window_.dataList.colorCount()
        self.main_window_.dataList.setWordWrap(True)
        self.main_window_.dataList.setColumnCount(len(headers_))
        self.main_window_.dataList.setRowCount(len(send_items_))
        self.main_window_.dataList.setHorizontalHeaderLabels(headers_)

        for row_idx_, si_ in enumerate(send_items_):
            try:
                self.main_window_.dataList.setCellWidget(row_idx_, 0, self.__build_preview_button(si_))

                for col_idx_ in range(1, len(headers_)):
                    self.main_window_.dataList.setItem(row_idx_, col_idx_, QTableWidgetItem(si_[headers_[col_idx_]]))

            except Exception as ex:
                traceback.print_exc()
                logging_emitter.error(str(ex))

        self.main_window_.dataList.resizeColumnsToContents()
        self.main_window_.dataList.resizeRowsToContents()

    def __build_preview_button(self, si_: dict[str, str]):
        btn_preview_ = QPushButton("Preview")
        btn_preview_.setFixedSize(50, 25)
        btn_preview_.pressed.connect(partial(self.preview_send_item, si_))
        return btn_preview_

    def preview_send_item(self, si_: dict[str, str]):
        try:
            if StringUtil.is_blank(self.main_window_.template_file_name_):
                raise IOError("template_file_name_ is None")

            preview_send_item(template_file_path_=self.main_window_.template_file_name_,
                              si_=si_)
        except Exception as ex:
            traceback.print_exc()
            logging_emitter.error(str(ex))

    def view_data(self):
        if StringUtil.is_blank(self.main_window_.data_file_name_):
            logging_emitter.error("data file is empty")
            return

        logging_emitter.info(f"viewing data file: {self.main_window_.data_file_name_}")
        os_util.os_open_file(self.main_window_.data_file_name_)

    def view_template(self):
        if StringUtil.is_blank(self.main_window_.template_file_name_):
            logging_emitter.error("template file is empty")
            return

        logging_emitter.info(f"viewing template file: {self.main_window_.template_file_name_}")
        os_util.os_open_file(self.main_window_.template_file_name_)
