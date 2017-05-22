from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QCheckBox, \
                           QComboBox, QHBoxLayout, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.label1 = QLabel("test1", self)
        combo1 = QComboBox(self)
        combo1.addItem('a')
        combo1.addItem('b')

        self.label1 = QLabel("test2", self)
        combo2 = QComboBox(self)
        combo2.addItem('c')
        combo2.addItem('d')

        hbox = QHBoxLayout()
        hbox.addWidget(combo1)
        hbox.addWidget(combo2)
        self.setLayout(hbox)
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Gwent Keg Tracker')
        self.show()
