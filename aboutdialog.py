from aboutdialog_ui import *
from PySide2 import QtGui
from PySide2 import QtCore

import ShotList_rc

class aboutDialog(QtWidgets.QDialog,Ui_Dialog):


    def __init__(self, parent=None):
        super(aboutDialog, self).__init__(parent)
        self.setupUi(self)

        self.mw = parent


        #gif表示
        self.setWindowTitle(self.tr("About {0}").format(self.mw.APPNAME))

        self.licfilepath = ""

        self.setWindowTitle(self.tr("About ShotList"))

        self.licfilepath = ":/txt/ShotListLic.txt"

        # self.plainTextEdit_info.appendPlainText(self.mw.APPNAME + " " + self.mw.__version__)
        # self.plainTextEdit_info.appendPlainText("")

        self.licfile = QtCore.QFile(self.licfilepath)
        self.licfile.open(QtCore.QFile.ReadOnly)
        #if (QtCore.QLocale.system().language() == QtCore.QLocale.Japanese):
        self.stream = QtCore.QTextStream(self.licfile)
        self.stream.setCodec("UTF-8")

        self.plainTextEdit_info.appendPlainText(self.stream.readAll())
        self.licfile.close()

        self.plainTextEdit_info.moveCursor(QtGui.QTextCursor.Start)
        self.plainTextEdit_info.ensureCursorVisible()
