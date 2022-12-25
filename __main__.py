import logging
import sys
import traceback

from PyQt6.QtWidgets import QApplication

from gui.stage.main_stage import MainWindow


def except_hook(exc_type, exc_value, exc_tb):
    error_stack_trace_ = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logging.error("error message:\n", error_stack_trace_)
    QApplication.quit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, encoding='utf-8', format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f"start running program")

    sys.excepthook = except_hook
    app = QApplication(sys.argv)

    main_window_ = MainWindow()
    main_window_.show()
    return_code_ = app.exec()
    sys.exit(return_code_)
