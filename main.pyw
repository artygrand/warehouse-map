#!/usr/bin/env python3

import os
import sys
import PyQt5

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from App.Main import MainWindow
from App.Data import Data


QApplication.addLibraryPath(os.path.join(os.path.dirname(PyQt5.__file__), 'Qt', 'plugins'))

app = QApplication(sys.argv)
app.setWindowIcon(QIcon('resource/favicon.png'))

Data.init('resource/database.db')

win = MainWindow('resource/map.svg', QSettings('resource/settings.ini', QSettings.IniFormat))
win.show()

sys.exit(app.exec_())
