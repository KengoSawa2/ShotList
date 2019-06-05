# -*- coding: utf-8 -*-

from PySide2 import QtWidgets

class StatusLabel(QtWidgets.QLabel):

    def __init__(self,parent=None):
        super(StatusLabel,self).__init__(parent)

    def minimumSizeHint(self):
        #sz = QtGui.QLabel.minimumSizeHint()
        sz = QtWidgets.QLabel.minimumSizeHint(self)
        sz.setWidth(0)
        return sz
