from PyQt6.QtWidgets import QTextEdit, QPushButton, QTableWidget, QWidget


class IMainStage(QWidget):
    data_file_name_: str | None = None

    inp_data_file_path_: QTextEdit
    btn_browse: QPushButton

    btn_load_data_: QPushButton

    btn_send_all_: QPushButton

    dataList: QTableWidget
