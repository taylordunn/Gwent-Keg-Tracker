import os
import json
import pandas as pd
import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QCheckBox, QPushButton, \
                            QComboBox, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, \
                            QTableWidget, QTableWidgetItem, QSizePolicy, \
                            QAbstractScrollArea, QMessageBox, QFileDialog


class MainWindow(QWidget):
    def __init__(self, cards_json):
        super().__init__()
        self.cards_json = cards_json
        self.init_ui()

    def init_ui(self):
        self.cards_df = self.load_cards()
        self.init_comboboxes()
        self.init_keg_interface()

        layout = QGridLayout()
        col_spacing = 2
        scale = 5

        # Use an additional scaling factor to fix the width of these lineedits
        scale2 = 1/2
        layout.addWidget(self.info_lineedit_list[0], 0, 0,
                         1, (2*col_spacing*scale-1)*scale2)
        layout.addWidget(self.info_lineedit_list[1], 0, 2*col_spacing*scale*scale2,
                         1, (2*col_spacing*scale-1)*scale2)
        layout.addWidget(self.info_lineedit_list[2], 0, 4*col_spacing*scale*scale2,
                         1, (2*col_spacing*scale-1)*scale2)
        layout.addWidget(self.info_lineedit_list[3], 0, 6*col_spacing*scale*scale2,
                         1, (2*col_spacing*scale-1)*scale2)


        combo_layout = [(1,0), (1,col_spacing),
                        (1,2*col_spacing), (1,3*col_spacing),
                        (2,col_spacing-1), (2,2*col_spacing-1),
                        (2,3*col_spacing-1)]
        for i,combo in enumerate(self.card_combobox_list):
            row,col = combo_layout[i] 

            layout.addWidget(combo, row, scale*col, 1, 2*scale-1)
            layout.addWidget(self.card_checkbox_list[i], row, (col+2)*scale-1)

        layout.addWidget(self.add_keg_button, row+1, 3*col_spacing + 2*scale,
                         1, 2*scale)
        layout.addWidget(self.keg_table, row+2, 0, 10, layout.columnCount())
        layout.addWidget(self.save_kegs_button, row+13, 3*col_spacing + scale,
                         1, 2*scale)
        layout.addWidget(self.load_kegs_button, row+13, 3*col_spacing + 3*scale, 1, 2*scale)
        

        self.setLayout(layout)
        self.setGeometry(200, 300, 500, 500)
        self.setWindowTitle('Gwent Keg Tracker')
        self.show()


    def init_comboboxes(self):
        self.info_lineedit_list = []
        self.card_combobox_list = []
        self.card_checkbox_list = []

        # Add a line for patch number
        lineedit = QLineEdit(self)
        lineedit.setPlaceholderText("Patch")
        self.info_lineedit_list.append(lineedit)
        # Add a line for prestige number
        lineedit = QLineEdit(self)
        lineedit.setPlaceholderText("Prestige")
        self.info_lineedit_list.append(lineedit)
        # Add a line for keg type
        lineedit = QLineEdit(self)
        lineedit.setPlaceholderText("Keg type")
        self.info_lineedit_list.append(lineedit)
        # Add a line for special events
        lineedit = QLineEdit(self)
        lineedit.setPlaceholderText("Special event")
        self.info_lineedit_list.append(lineedit)

        # Filter out Leaders
        #nonleader_cards_df = self.cards_df[self.cards_df.category != 'Leader']
        nonleader_cards_df = self.cards_df[self.cards_df.color != 'leader']

        for i in range(4):
            combo = QComboBox(self)
            combo.setEditable(True)
            # Add an empty item so that nothing is selected to begin
            combo.addItem("")
            combo.addItems(nonleader_cards_df.index.values)
            combo.lineEdit().setPlaceholderText("Card %d" % (i+1))
            self.card_combobox_list.append(combo)
            self.card_checkbox_list.append(QCheckBox(self))

        combo_text = ['Picked card', 'Unpicked card 1', 'Unpicked card 2']
        rare_cards_df = nonleader_cards_df[nonleader_cards_df.rarity.isin(['rare', 'epic', 'legendary'])]

        for i in range(3):
            combo = QComboBox(self)
            combo.setEditable(True)
            combo.addItem("")
            combo.addItems(rare_cards_df.index.values)
            combo.lineEdit().setPlaceholderText(combo_text[i])
            self.card_combobox_list.append(combo)
            self.card_checkbox_list.append(QCheckBox(self))

    def init_keg_interface(self):
        self.add_keg_button = QPushButton("Add Keg")
        self.add_keg_button.clicked.connect(self.add_keg)

        self.keg_table = QTableWidget()
        self.keg_table.setRowCount(0)
        self.keg_table.setColumnCount(7)
        self.keg_table.setHorizontalHeaderLabels(['Card 1', 'Card 2',
            'Card 3', 'Card 4', 'Picked card',
            'Unpicked card 1', 'Unpicked card 2'])
        self.keg_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.keg_table.resizeColumnsToContents()

        if os.path.isfile('kegs.csv'):
            self.keg_df = pd.read_csv('kegs.csv')
            self.update_table()
            # If kegs data exist, use the latest entry to replace placeholder text in the LineEdits
            if len(self.keg_df) > 0:
                for i,var in enumerate(['patch', 'prestige', 'keg_type', 'event']):
                    if not pd.isna(self.keg_df[var][0]):
                        self.info_lineedit_list[i].setText(str(self.keg_df[var][0]))
        else:
            self.keg_df = pd.DataFrame(columns=['date', 'patch', 'prestige', 'keg_type', 'event', 'card1', 'card2',
                                                'card3', 'card4', 'picked_card', 'unpicked_card1', 'unpicked_card2'])

        self.save_kegs_button = QPushButton("Save Kegs")
        self.save_kegs_button.clicked.connect(self.save_kegs)
        self.load_kegs_button = QPushButton("Load Kegs")
        self.load_kegs_button.clicked.connect(self.load_kegs)

    def add_keg(self):
        """
        In response to the button 'Add Keg', append a new list of cards and
        datetime to the keg_df dataframe, then update the table.
        """
        card_names = []
        for i in range(7):
            card_name = self.card_combobox_list[i].currentText()

            if card_name not in self.cards_df.index.values:
                error_message = QMessageBox()
                error_message.setText("Card %d invalid." % (i+1))
                error_message.setWindowTitle("Error")
                error_message.setStandardButtons(QMessageBox.Ok)# | \
                                                 #QMessageBox.Cancel)
                error_message.exec_()
                return
            else:
                if self.card_checkbox_list[i].checkState() == Qt.Checked:
                    # Use an asterisk to denote premium cards
                    card_name += "*"
                card_names.append(card_name)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        patch = self.info_lineedit_list[0].text()
        prestige = self.info_lineedit_list[1].text()
        keg_type = self.info_lineedit_list[2].text()
        event = self.info_lineedit_list[3].text()
        card_names.insert(0, time)
        card_names.insert(1, patch)
        card_names.insert(2, prestige)
        card_names.insert(3, keg_type)
        card_names.insert(4, event)
        self.keg_df = self.keg_df.append(pd.DataFrame([card_names], columns=self.keg_df.columns))
        self.keg_df.to_csv('kegs_backup.csv', index=False)
        self.update_table()

        # Reset card text fields and check boxes
        for i in range(7):
            self.card_combobox_list[i].setCurrentText("")
            self.card_checkbox_list[i].setChecked(False)

    def update_table(self):
        """
        Sort keg_df by date and repopulate the rows of keg_table.
        """
        self.keg_df.date = pd.to_datetime(self.keg_df.date)
        self.keg_df.sort_values(by='date', ascending=False, inplace=True)
        self.keg_df.index = range(len(self.keg_df.index))

        self.keg_table.clear()
        self.keg_table.setRowCount(len(self.keg_df.index))

        for row,keg in self.keg_df.iterrows():
            cards = [keg[s] for s in ['card1', 'card2', 'card3',
                                           'card4', 'picked_card',
                                           'unpicked_card1', 'unpicked_card2']]
            for col,card in enumerate(cards):
                self.keg_table.setItem(row, col, QTableWidgetItem(card))
        self.keg_table.resizeColumnsToContents()


    def load_cards(self):
        """
        Opens the specified JSON file containing card details (name, category
        and rarity). Returns a pandas dataframe of the data.
        """
        with open(self.cards_json) as infile:
            cards = json.load(infile)
            infile.close()

        cards_dict = {}
        cards_dict['name'] = [card['name'] for card in cards]
        #cards_dict['category'] = [card['category'] for card in cards]
        cards_dict['color'] = [card['color'] for card in cards]
        cards_dict['rarity'] = [card['rarity'] for card in cards]

        df = pd.DataFrame(cards_dict)
        df.sort_values(by='name', ascending=True, inplace=True)
        df.set_index('name', inplace=True)
        return df

    def save_kegs(self):
        try:
            name = QFileDialog.getSaveFileName(self, 'Save file')
            self.keg_df.to_csv(name[0], index=False)
        except BaseException as e:
            error_message = QMessageBox()
            error_message.setText("Save file failed: " + str(e))
            error_message.setWindowTitle("Error")
            error_message.setStandardButtons(QMessageBox.Ok)
            error_message.exec_()

    def load_kegs(self):
        try:
            name = QFileDialog.getOpenFileName(self, 'Open file')
            self.keg_df = pd.read_csv(name[0])
            self.update_table()
        except BaseException as e:
            error_message = QMessageBox()
            error_message.setText("Load file failed: " + str(e))
            error_message.setWindowTitle("Error")
            error_message.setStandardButtons(QMessageBox.Ok)
            error_message.exec_()
