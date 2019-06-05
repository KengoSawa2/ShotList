# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutdialog_ui.ui',
# licensing of 'aboutdialog_ui.ui' applies.
#
# Created: Sun Jun  2 18:59:42 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(5, 0, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEdit_info = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit_info.setObjectName("plainTextEdit_info")
        self.gridLayout.addWidget(self.plainTextEdit_info, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))

