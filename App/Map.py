#!/usr/bin/env python3

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QDialog, QGraphicsRectItem, QGraphicsScene, QGraphicsView, QVBoxLayout, QGraphicsPathItem
from PyQt5.QtXml import QDomDocument


class MapDialog(QDialog):
    def __init__(self, map_file, cell, settings):
        super().__init__()
        self.setWindowTitle('Карта')
        self.setModal(True)
        size = settings.value('dialogs/map').split(' ')
        self.setFixedSize(int(size[0]), int(size[1]))

        self.cell = cell

        reader = SvgReader(map_file)
        scene = QGraphicsScene()
        scene.setSceneRect(reader.get_size())

        coord = settings.value('map/{}'.format(cell)).split(' ')
        for rect in reader.get_elements(coord[0], int(coord[1])):
            scene.addItem(rect)

        layout = QVBoxLayout(self)
        layout.addWidget(QGraphicsView(scene))


class SvgReader:
    def __init__(self, file):
        self.doc = QDomDocument()
        with open(file) as svg:
            self.doc.setContent(svg.read())

    def get_elements(self, cell, height):
        result = []
        current = []

        rectangles = self.doc.elementsByTagName('rect')

        for i in range(rectangles.size()):
            rect = rectangles.item(i).toElement()
            fill = '#aaaaaa'

            item = QGraphicsRectItem(float(rect.attribute('x')), float(rect.attribute('y')),
                                     float(rect.attribute('width')), float(rect.attribute('height')))
            item.setBrush(QBrush(QColor(fill)))
            result.append(item)

            if rect.attribute('id') == str(cell):
                side_fill = fill
                size = item.rect().getRect()

                for j in range(1, height+1):
                    x = size[0] - 12 * j
                    y = size[1] - 20 * j

                    if j == height:
                        side_fill = '#ff0000'
                        top = QGraphicsRectItem(x, y, size[2], size[3])
                        top.setBrush(QBrush(QColor(fill).darker(200)))
                        current.append(top)

                    path = QPainterPath()
                    path.moveTo(x + size[2], y + size[3])
                    path.lineTo(x + size[2] + 12, y + size[3] + 20)
                    path.lineTo(x + 12, y + size[3] + 20)
                    path.lineTo(x, y + size[3])
                    front = QGraphicsPathItem(path)
                    front.setBrush(QBrush(QColor(side_fill)))
                    current.append(front)

                    path = QPainterPath()
                    path.moveTo(x + size[2], y + size[3])
                    path.lineTo(x + size[2] + 12, y + size[3] + 20)
                    path.lineTo(x + size[2] + 12, y + 20)
                    path.lineTo(x + size[2], y)
                    right = QGraphicsPathItem(path)
                    right.setBrush(QBrush(QColor(side_fill).lighter()))
                    current.append(right)

        return result + current

    def get_size(self):
        svg = self.doc.elementsByTagName('svg')
        if svg.size() > 0:
            param = svg.item(0).toElement().attribute('viewBox').split(' ')
            return QRectF(int(float(param[0])), int(float(param[1])), int(float(param[2])), int(float(param[3])))

        return QRectF(0, 0, 400, 400)
