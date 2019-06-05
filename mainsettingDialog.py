# -*- coding: utf-8 -*-

import platform
import mainwindow as mw

sysisDarwin = platform.system() == 'Darwin'
sysisWindows = platform.system() == 'Windows'

if sysisDarwin:
    from Foundation import NSURL
    from Foundation import NSString
else:
    from knownpaths import *

from mainsettingdialog_ui import *

from PySide2 import QtGui
from PySide2 import QtCore

from PySide2.QtCore import Qt

from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtCore import QSettings
from PySide2.QtCore import QObject
from PySide2.QtCore import QDateTime
from PySide2.QtCore import QUrl

from pprint import pprint

class mainSettingDialog(QtWidgets.QDialog,Ui_mainsettingDialog):

    def __init__(self, parent=None,isjp=None):
        super(mainSettingDialog, self).__init__(parent)

        self.setupUi(self)
        self.mw = parent
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setWindowTitle(self.mw.APPNAME)

        self.__initEv()
        self.__readsettings()
        self.listWidget_Options.setCurrentRow(0)

    def __initEv(self):

        # self.buttonBox.accepted.connect(self.__accepted)
        # self.buttonBox.rejected.connect(self.__accepted)
        self.pushButton_save.clicked.connect(self.__accepted)
        self.pushButton_cancel.clicked.connect(self.__rejected)

        # self.pushButton_restore.clicked.connect(self.__restore)
        self.pushButton_all_restore.clicked.connect(self.__restore_all)
        self.pushButton_restore_columns.clicked.connect(self.__restore_columns)
        self.pushButton_restore_thumb.clicked.connect(self.__restore_thumb)
        self.pushButton_restore_xlsx.clicked.connect(self.__restore_xlsx)
        self.pushButton_restore_misc.clicked.connect(self.__restore_misc)

        self.pushButton_add.clicked.connect(self.__add)
        self.pushButton_remove.clicked.connect(self.__remove)
        self.pushButton_up.clicked.connect(self.__up)
        self.pushButton_down.clicked.connect(self.__down)
        self.pushButton_eyecatch.clicked.connect(self.__input_clicked)
        self.listWidget_Options.currentRowChanged.connect(self.__optionchanged)

        self.listWidget_mod.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget_org.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        # self.radioButton_book.toggled.connect(self.groupBox_xlsxout)
        # self.radioButton_sheet.toggled.connect(self.groupBox_xlsxout)
        # self.radioButton_all.toggled.connect(self.groupBox_xlsxout)
        # print(self.groupBox_xlsxout.toggled.connect(self.__xlsx_toggled))

        self.spinBox_maxrows.setMinimum(0)
        self.spinBox_maxrows.setMaximum(65535)
        self.radioButton_book.toggled.connect(self.__xlsx_toggled_book)
        self.radioButton_sheet.toggled.connect(self.__xlsx_toggled_sheet)
        self.radioButton_all.toggled.connect(self.__xlsx_toggled_all)

        # workaround for PySide2 and Mojave bug
        self.pushButton_up.setVisible(False)
        self.pushButton_down.setVisible(False)

        return

    def __readsettings(self):
        for columnname in self.mw.def_columnlist:
            if columnname in self.mw.columnlist:
                self.listWidget_mod.addItem(columnname)
            else:
                self.listWidget_org.addItem(columnname)

        # self.lineEdit_x.setText(str(self.mw.cfg.value(self.mw.OPT_THUMBNAIL_X,self.mw.THUMBNAIL_DEFAULT_X)))
        # self.lineEdit_y.setText(str(self.mw.cfg.value(self.mw.OPT_THUMBNAIL_Y,self.mw.THUMBNAIL_DEFAULT_Y)))
        # self.lineEdit_Bright.setText(str(self.mw.cfg.value(self.mw.OPT_THUMBNAIL_BRIGHT,self.mw.THUMBNAIL_DEFALUT_BRIGHT)))
        # self.lineEdit_Start.setText(str(self.mw.cfg.value(self.mw.OPT_THUMBNAIL_OFF_S,self.mw.THUMBNAIL_DEFAULT_OFF_S)))
        self.lineEdit_x.setText(str(self.mw.thumbnail_x))
        self.lineEdit_y.setText(str(self.mw.thumbnail_y))
        self.lineEdit_Bright.setText(str(self.mw.thumbnail_bright))
        self.lineEdit_Start.setText(str(self.mw.startoffset))
        self.lineEdit_Center.setText(str(self.mw.centeroffset))
        self.lineEdit_End.setText(str(self.mw.endoffset))
        self.lineEdit_stafps.setText(str(self.mw.stafps))
        self.checkBox_Disableseq.setChecked(self.mw.disableseq)
        self.comboBox_checksum.findText(str(self.mw.CHECK_ALGO_XXHASH))
        self.lineEdit_eyecatch.setText(str(self.mw.eyecatch))
        if self.mw.xlsxouttype == 0:
            self.radioButton_book.setChecked(True)
        elif self.mw.xlsxouttype == 1:
            self.radioButton_sheet.setChecked(True)
        else:
            self.radioButton_all.setChecked(True)
        self.spinBox_maxrows.setValue(self.mw.xlsxmaxrows)
        if self.mw.lcid == QtCore.QLocale.Japanese:
            self.checkBox_lang.setChecked(True)
        else:
            self.checkBox_lang.setChecked(False)
        return

    def __writesettings(self):
        self.mw.thumbnail_x = int(self.lineEdit_x.text())
        self.mw.thumbnail_y = int(self.lineEdit_y.text())
        self.mw.thumbnail_bright = float(self.lineEdit_Bright.text())
        self.mw.startoffset = float(self.lineEdit_Start.text())
        self.mw.centeroffset = float(self.lineEdit_Center.text())
        self.mw.endoffset = float(self.lineEdit_End.text())
        self.mw.stafps = float(self.lineEdit_stafps.text())
        self.mw.disableseq = self.checkBox_Disableseq.isChecked()
        self.mw.checksumalgo = self.comboBox_checksum.currentText()
        self.mw.eyecatch = self.lineEdit_eyecatch.text()
        self.mw.xlsxmaxrows = self.spinBox_maxrows.value()

        if self.checkBox_lang.isChecked():
            self.mw.lcid = QtCore.QLocale.Japanese
        else:
            self.mw.lcid = 0

        self.mw.cfg.setValue(self.mw.OPT_COLUMNLIST,self.mw.columnlist)
        self.mw.cfg.setValue(self.mw.OPT_THUMB_X,self.lineEdit_x.text())
        self.mw.cfg.setValue(self.mw.OPT_THUMB_Y,self.lineEdit_y.text())
        self.mw.cfg.setValue(self.mw.OPT_THUMB_BRIGHT, self.lineEdit_Bright.text())
        self.mw.cfg.setValue(self.mw.OPT_THUMB_OFF_S, self.lineEdit_Start.text())
        self.mw.cfg.setValue(self.mw.OPT_THUMB_OFF_C, self.lineEdit_Center.text())
        self.mw.cfg.setValue(self.mw.OPT_THUMB_OFF_E, self.lineEdit_End.text())

        self.mw.cfg.setValue(self.mw.OPT_STAFPS,self.lineEdit_stafps.text())
        self.mw.cfg.setValue(self.mw.OPT_CHECK_ALGO,self.comboBox_checksum.currentText())
        self.mw.cfg.setValue(self.mw.OPT_EYECATCH,self.mw.eyecatch)
        self.mw.cfg.setValue(self.mw.OPT_XLSXOUTTYPE, self.mw.xlsxouttype)
        self.mw.cfg.setValue(self.mw.OPT_XLSXMAXROWS,self.mw.xlsxmaxrows)
        self.mw.cfg.setValue(self.mw.OPT_LCID,self.mw.lcid)

    def __accepted(self):

        modlist = []
        for index in range(self.listWidget_mod.count()):
            text = self.listWidget_mod.item(index).text()
            # self.mw.columnlist.append(text)
            modlist.append(text)

        if self.mw.columnlist != modlist:
            if self.mw.tableWidget_shotlist.rowCount():
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Question)
                msgBox.setText(self.tr("Current Columns and Rows will be Delete.\nAre you sure?"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if (msgBox.exec_() == QtWidgets.QMessageBox.No):
                    return

            self.mw.columnlist.clear()
            for index in range(self.listWidget_mod.count()):
                text = self.listWidget_mod.item(index).text()
                self.mw.columnlist.append(text)
            self.mw.tableWidget_shotlist.clearContents()
            self.mw.tableWidget_shotlist.setRowCount(0)
            self.mw.tableWidget_shotlist.setColumnCount(len(self.mw.columnlist))
            self.mw.tableWidget_shotlist.setHorizontalHeaderLabels(self.mw.columnlist)

        self.__writesettings()
        # print("__accepted")
        self.accept()

    def __rejected(self):
        self.reject()

    def __restore_columns(self):
        self.msgBox.setIcon(QtWidgets.QMessageBox.Question)
        self.msgBox.setText(self.tr("Restore default Columns settings?"))
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if (self.msgBox.exec_() == QtWidgets.QMessageBox.Yes):
            self.listWidget_mod.clear()
            self.listWidget_org.clear()
            for columnname in self.mw.def_columnlist:
                if columnname not in self.mw.def_nodefaultlist:
                    self.listWidget_mod.addItem(columnname)
                else:
                    self.listWidget_org.addItem(columnname)

    def __restore_thumb(self):
        self.msgBox.setIcon(QtWidgets.QMessageBox.Question)
        self.msgBox.setText(self.tr("Restore default Thumbnail settings?"))
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if (self.msgBox.exec_() == QtWidgets.QMessageBox.Yes):
            self.lineEdit_x.setText(str(self.mw.THUMB_DEFAULT_X))
            self.lineEdit_y.setText(str(self.mw.THUMB_DEFAULT_Y))
            self.lineEdit_Bright.setText(str(self.mw.THUMB_DEFALUT_BRIGHT))
            self.lineEdit_Start.setText(str(self.mw.THUMB_DEFAULT_OFF))
            self.lineEdit_Center.setText(str(self.mw.THUMB_DEFAULT_OFF))
            self.lineEdit_End.setText(str(self.mw.THUMB_DEFAULT_OFF_E))
            self.lineEdit_stafps.setText(str(self.mw.STAFPS_DEFAULT))

    def __restore_xlsx(self):
        self.msgBox.setIcon(QtWidgets.QMessageBox.Question)
        self.msgBox.setText(self.tr("Restore default Xlsx settings?"))
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if (self.msgBox.exec_() == QtWidgets.QMessageBox.Yes):
            self.__xlsx_toggled_all(True)

    def __restore_misc(self):
        self.msgBox.setIcon(QtWidgets.QMessageBox.Question)
        self.msgBox.setText(self.tr("Restore default Misc settings?"))
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if (self.msgBox.exec_() == QtWidgets.QMessageBox.Yes):
            self.checkBox_Disableseq.setChecked(False)
            self.comboBox_checksum.setCurrentIndex(0)
            self.lineEdit_eyecatch.setText("")
            if int(QtCore.QLocale.system().language()) == QtCore.QLocale.Japanese:
                self.checkBox_lang.setChecked(True)
            else:
                self.checkBox_lang.setChecked(False)

    def __restore_all(self):

        self.msgBox.setIcon(QtWidgets.QMessageBox.Question)
        self.msgBox.setText(self.tr("Restore ALL default settings?"))
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if (self.msgBox.exec_() == QtWidgets.QMessageBox.Yes):

            self.listWidget_mod.clear()
            self.listWidget_org.clear()
            for columnname in self.mw.def_columnlist:
                if columnname not in self.mw.def_nodefaultlist:
                    self.listWidget_mod.addItem(columnname)
                else:
                    self.listWidget_org.addItem(columnname)

            self.lineEdit_x.setText(str(self.mw.THUMB_DEFAULT_X))
            self.lineEdit_y.setText(str(self.mw.THUMB_DEFAULT_Y))
            self.lineEdit_Bright.setText(str(self.mw.THUMB_DEFALUT_BRIGHT))
            self.lineEdit_Start.setText(str(self.mw.THUMB_DEFAULT_OFF))
            self.lineEdit_Center.setText(str(self.mw.THUMB_DEFAULT_OFF))
            self.lineEdit_End.setText(str(self.mw.THUMB_DEFAULT_OFF_E))
            self.lineEdit_stafps.setText(str(self.mw.STAFPS_DEFAULT))
            self.checkBox_Disableseq.setChecked(False)
            self.comboBox_checksum.setCurrentIndex(0)
            self.lineEdit_eyecatch.setText("")
            self.__xlsx_toggled_all(True)
            if int(QtCore.QLocale.system().language()) == QtCore.QLocale.Japanese:
                self.checkBox_lang.setChecked(True)
            else:
                self.checkBox_lang.setChecked(False)
            pass

    def __add(self):
        index = self.listWidget_org.currentRow()
        if index == -1:
            return
        item = self.listWidget_org.takeItem(index)

        insertindex = self.listWidget_mod.currentRow()
        if insertindex == -1:
            insertindex = self.listWidget_mod.count() - 1
        self.listWidget_mod.insertItem(insertindex,item)

    def __remove(self):
        index = self.listWidget_mod.currentRow()
        if index == -1 or self.listWidget_mod.count() < 2:
            return
        item = self.listWidget_mod.takeItem(index)
        self.listWidget_org.insertItem(0,item)

    def __up(self):

        index = self.listWidget_mod.currentRow()
        # no selected
        if index == -1 or index == 0:
            return
        item = self.listWidget_mod.takeItem(index)
        self.listWidget_mod.insertItem(index - 1,item)
        self.listWidget_mod.setCurrentItem(item)

    def __down(self):

        index = self.listWidget_mod.currentRow()

        # no selected
        if index == -1 or index + 1 >= self.listWidget_mod.count():
            return
        item = self.listWidget_mod.takeItem(index)
        self.listWidget_mod.insertItem(index + 1,item)
        self.listWidget_mod.setCurrentItem(item)

    def __optionchanged(self, rowindex):
        self.stackedWidget_Options.setCurrentIndex(rowindex)

    def __input_clicked(self):

        # filterstr = ["Image files(*.png *.jpg *.jpeg)"]
        #filedialog = QFileDialog()
        # filedialog.setNameFilters(filterstr)
        # file_path = QFileDialog.getOpenFileName(self,self.tr("Open Image File"),"",self.tr("Image Files (*.png *.jpg *.jpeg)"))
        file_path = QFileDialog.getOpenFileName(self,self.tr("Open Image File"),"","Image Files (*.png *.jpg *.jpeg)")

        if not file_path:
            # print("no selected")
            return
        else:
            # getOpenFileName retured tuple... PySide1 bug?
            self.lineEdit_eyecatch.setText(file_path[0])
        return

    def __xlsx_toggled_book(self,checked):
        if checked:
            self.spinBox_maxrows.setEnabled(True)
            self.spinBox_maxrows.setValue(100)
            self.radioButton_book.setChecked(True)
            self.mw.xlsxouttype = 0

    def __xlsx_toggled_sheet(self,checked):
        if checked:
            self.spinBox_maxrows.setEnabled(True)
            self.spinBox_maxrows.setValue(100)
            self.radioButton_sheet.setChecked(True)
            self.mw.xlsxouttype = 1

    def __xlsx_toggled_all(self,checked):
        if checked:
            self.spinBox_maxrows.setValue(0)
            self.spinBox_maxrows.setEnabled(False)
            self.radioButton_all.setChecked(True)
            self.mw.xlsxouttype = 2

    def closeEvent(self,cevent):
        return self.Rejected
