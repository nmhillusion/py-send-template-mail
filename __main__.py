import logging
import sys

from PyQt6.QtWidgets import QApplication

from gui.main_stage import MainWindow

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, encoding='utf-8', format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f"start running program")
    # main.run()

    app = QApplication(sys.argv)
    main_window_ = MainWindow()
    main_window_.show()
    sys.exit(app.exec())
