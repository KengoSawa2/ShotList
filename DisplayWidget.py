# -*- coding: utf-8 -*-

from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2.QtCore import Qt

class DisplayWidget(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(DisplayWidget, self).__init__(parent)
        #self.setScaledContents(True)
        self.setMinimumSize(1920 / 10, 1080 / 10)

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHeightForWidth(True)

        self.setSizePolicy(size_policy)

        self.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        self.pixmap = None
        self.setMargin(10)

    def heightForWidth(self, width):
        return width * 9 / 16.0

    @QtCore.Slot(object, object)
    def setPixmap(self, img, index):
        #if index == self.current_index:
        self.pixmap = QtGui.QPixmap.fromImage(img)

        #super(DisplayWidget, self).setPixmap(self.pixmap)
        super(DisplayWidget, self).setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def sizeHint(self):
        width = self.width()
        return QtCore.QSize(width, self.heightForWidth(width))

    def resizeEvent(self, event):
        if self.pixmap:
            super(DisplayWidget, self).setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def sizeHint(self):
        return QtCore.QSize(1920 / 2.5, 1080 / 2.5)