import sys
from PyQt5.QtWidgets import QApplication
from gwent_keg_tracker.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow("cards.json")
    sys.exit(app.exec_())
