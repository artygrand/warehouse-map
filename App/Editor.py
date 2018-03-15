#!/usr/bin/env python3

from PyQt5.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton

from App.Data import Data


class EditorDialog(QDialog):
    def __init__(self, id, title):
        super().__init__()

        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(600, 250)

        self.id = id
        item = Data.read(id) if id > 0 else (0, '', '', '', '')

        self.inputs = {
            'cell': QLineEdit(str(item[1])),
            'title': QLineEdit(item[2]),
            'quantity': QLineEdit(str(item[3])),
            'description': QTextEdit(item[4]),
        }

        form = QFormLayout(self)
        form.addRow('Название', self.inputs['title'])
        form.addRow('Количество', self.inputs['quantity'])
        form.addRow('Ячейка', self.inputs['cell'])
        form.addRow('Описание или<br>ключевые слова', self.inputs['description'])

        buttons = QHBoxLayout()
        buttons.addStretch()
        if self.id > 0:
            btn = QPushButton('Удалить')
            btn.clicked.connect(self.delete)
            buttons.addWidget(btn)

        btn = QPushButton('Сохранить')
        btn.setDefault(True)
        btn.clicked.connect(self.save)
        buttons.addWidget(btn)

        form.addRow(buttons)

    def save(self):
        data = {
            'title': self.inputs['title'].text(),
            'quantity': self.inputs['quantity'].text(),
            'cell': self.inputs['cell'].text(),
            'description': self.inputs['description'].toPlainText()
        }

        if self.id > 0:
            data['id'] = self.id
            Data.update(data)
        else:
            Data.create(data)

        self.accept()

    def delete(self):
        Data.delete(self.id)
        self.accept()
