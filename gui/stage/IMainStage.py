from PyQt6.QtWidgets import QTextEdit, QPushButton, QTableWidget, QWidget


class IMainStage(QWidget):
    data_file_name_: str | None = None
    template_file_name_: str | None = None

    inp_data_file_path_: QTextEdit
    btn_browse__data: QPushButton

    inp_template_mail_file_path_: QTextEdit
    btn_browse__template: QPushButton

    btn_load_data_: QPushButton

    btn_send_all_: QPushButton

    dataList: QTableWidget

    def re_enable_action_buttons(self):
        pass
