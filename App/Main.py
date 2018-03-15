#!/usr/bin/env python3

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QFormLayout, \
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLabel

from App.Editor import EditorDialog
from App.Map import MapDialog
from App.Data import Data


class MainWindow(QMainWindow):
    def __init__(self, map_file, settings):
        super().__init__()
        self.setWindowTitle('Карта склада')
        self.setMinimumSize(QSize(600, 480))
        size = settings.value('dialogs/main').split(' ')
        self.resize(int(size[0]), int(size[1]))

        self.modal = None
        self.map_file = map_file
        self.settings = settings

        self.init_menu_bar()
        self.init_status_bar()
        self.init_content()

    def init_menu_bar(self):
        menu = self.menuBar()

        act = QAction('&Добавить новый предмет', self)
        act.setShortcut('Ctrl+N')
        act.triggered.connect(self.open_editor)
        menu.addAction(act)

    def init_status_bar(self):
        self.statusBar().showMessage('Ready')

    def init_content(self):
        main = QWidget()
        self.setCentralWidget(main)

        self.layout = QVBoxLayout(main)

        self.input = QLineEdit()
        self.input.returnPressed.connect(self.update_list)
        search = QFormLayout()
        search.addRow('Название или ключевое слово', self.input)
        self.layout.addLayout(search)
        self.update_list()

    def update_list(self):
        self.clear_result()

        data = Data.find(self.input.text())

        self.layout.addWidget(self.make_table(data))
        self.statusBar().showMessage('Найдено: {}'.format(len(data)))

    def clear_result(self):
        self.statusBar().clearMessage()

        w = self.layout.takeAt(1)
        if w is not None:
            w.widget().deleteLater()

    def make_table(self, data):
        table = QTableWidget(len(data), 3)
        table.setHorizontalHeaderLabels(['Название', 'Кол-во', 'Ячейка'])

        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.setColumnWidth(1, 80)
        table.setColumnWidth(2, 150)

        for i, row in enumerate(data):
            table.setItem(i, 0, readonly_cell(row[2], row[0], row[1]))
            table.setItem(i, 1, readonly_cell(row[3], row[0], row[1]))
            table.setCellWidget(i, 2, self.cell_btn(row[1]))

        table.itemClicked.connect(self.open_editor)

        return table

    def open_editor(self, item=None):
        if type(item) is QTableWidgetItem:
            id = int(item.id)
            title = 'Редактирование предмета'
        else:
            id = 0
            title = 'Добавление предмета'

        self.modal = EditorDialog(id, title)
        self.modal.show()
        self.modal.accepted.connect(self.update_list)

    def open_map(self):
        self.modal = MapDialog(self.map_file, self.sender().cell, self.settings)
        self.modal.show()

    def cell_btn(self, cell):
        lay = QHBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)

        lay.addWidget(QLabel(str(cell)), alignment=Qt.AlignCenter)

        b = QPushButton('На карте')
        b.clicked.connect(self.open_map)
        b.cell = cell
        lay.addWidget(b, alignment=Qt.AlignCenter)

        w = QWidget()
        w.setLayout(lay)

        return w


def readonly_cell(text, id, cell):
    item = QTableWidgetItem(str(text))
    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
    item.id = id
    item.cell = cell

    return item

