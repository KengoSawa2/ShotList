# -*- coding: utf-8 -*-
import platform
import os
import datetime
import subprocess
import sys
import dateutil.parser
import pprint as pp
import codecs
import math

sysisDarwin = platform.system() == 'Darwin'

if sysisDarwin:
    from Foundation import NSURL
    from Foundation import NSString

from mainwindow_ui import *
from mainsettingDialog import *
from aboutdialog import *

from shotlist import ShotList

from StatusLabel import StatusLabel
from VideoPlayerDialog import VideoPlayerDialog
from SequencePlayerDialog import SequencePlayerDialog
from FrameGrabber import FrameGrabber

from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore

from PySide2.QtCore import Qt

from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtCore import QSettings
from PySide2.QtCore import QObject
from PySide2.QtCore import QDateTime
from PySide2.QtCore import QUrl
from PySide2.QtCore import QStandardPaths

import pyseq

from PySide2.QtGui import QDesktopServices
import PIL

class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):

    '''
    ShotList MainWindow
    '''

    APPNAME = "shotlist"
    APPID   = "com.LespaceVision.ShotList"
    __version__ = "1.1.3"

    # ShotList Column Name define
    NO = 'No.'
    THUMB_S = 'Start Frame'
    THUMB_C = 'Center Frame'
    THUMB_E = 'End Frame'
    FILENAME = 'FileName'
    SCENE = 'Scene'
    CUT = 'Cut'
    TAKE = 'Take'
    COMMENT = 'Comment'
    CONTAINER = 'Container'
    CODEC = 'Codec'
    PIXSIZE = 'Resolution'
    FILESIZE_GB = 'filesize(GB)'
    FILESIZE_MB = 'filesize(MB)'
    REEL = 'Reel'
    FPS = 'fps'
    SENSORFPS = 'SensorFps'
    LENGTH ='Duration'
    TC = 'StartTC'
    BIT = 'bit'
    ALPHA = 'alpha'
    COLORSPACE = 'colorspace'
    GAMMA = 'gamma'
    AUDIOCH = 'Audio ch'
    AUDIOSRATE = 'Audio rate'
    AUDIOCODEC = 'Audio codec'
    AUDIOBRATE = 'Audio bitrate'
    CREATETIME = 'Create Time'
    FULLPATH = 'fullpath'
    RELPATH = 'relpath'
    CHECKSUM = 'checksum'
    CHECKSUM_XXHASH = 'checksum(xxHash)'
    CHECKSUM_MD5 = 'checksum(MD5)'
    CHECKSUM_SHA1 = 'checksum(SHA1)'
    EXINFO = 'Exinfo'

    # hidden data
    DIRPATH_HIDDEN = 'base_hidden'
    FILENAME_HIDDEN = 'name_hidden'

    SEQPATH_HIDDEN = 'seq_hidden'
    SEQ_HIDDEN_S = 'seq_hidden_s'
    SEQ_HIDDEN_C = 'seq_hidden_c'
    SEQ_HIDDEN_E = 'seq_hidden_e'

    CHECK_ALGO_SHA1 = "(SHA1)"     # RapidCopy cfg.usemd5=0
    CHECK_ALGO_MD5 = "(MD5)"       # RapidCopy cfg.usemd5=1
    CHECK_ALGO_XXHASH = "(xxHash)" # RapidCopy cfg.usemd5=2

    #Specification follows RapidCopy.See RapdiCopy source cfg.usemd5...
    CHECK_ALGO_DICT = {0:CHECK_ALGO_SHA1,1:CHECK_ALGO_MD5,2:CHECK_ALGO_XXHASH}

    SeqRole = QtCore.Qt.UserRole + 1

    #ShotList Column list
    def_columnlist = [
        NO,THUMB_S,THUMB_C,THUMB_E,FILENAME,SCENE,CUT,TAKE,COMMENT,CONTAINER,CODEC,PIXSIZE,FILESIZE_GB,FILESIZE_MB,
        REEL,FPS,SENSORFPS,LENGTH,TC,BIT,ALPHA,COLORSPACE,GAMMA,AUDIOCH,AUDIOSRATE,AUDIOCODEC,AUDIOBRATE,
        CREATETIME,FULLPATH,RELPATH,CHECKSUM,EXINFO
    ]
    #ShotList no default Column list
    def_nodefaultlist = [
        THUMB_S,THUMB_E,CHECKSUM,FILESIZE_MB,SENSORFPS
    ]

    #ShotList Column defaults data
    # key=Column name
    # value = column propetry list
    # [0]:itemrole  method(int)        0:DisplayRole,1:DecorationRole,2:NoRole
    # [1]:dataset   method(int)        0:item.setText,1:item.setData,
    # [2]:itemflags Qt::ItemFlags(int) 33:select&enable 35:33+edit

    def_columnpropdict = {
                            NO          : [Qt.DisplayRole, 1, 35],
                            THUMB_S     : [Qt.DecorationRole, 1, 33],
                            THUMB_C     : [Qt.DecorationRole, 1, 33],
                            THUMB_E     : [Qt.DecorationRole, 1, 33],
                            FILENAME    : [Qt.DisplayRole, 0, 33],
                            SCENE       : [Qt.DisplayRole, 0, 35],
                            CUT         : [Qt.DisplayRole, 0, 35],
                            TAKE        : [Qt.DisplayRole, 0, 35],
                            COMMENT     : [Qt.DisplayRole, 0, 35],
                            CONTAINER   : [Qt.DisplayRole, 0, 33],
                            CODEC       : [Qt.DisplayRole, 0, 33],
                            PIXSIZE     : [Qt.DisplayRole, 0, 33],
                            FILESIZE_GB : [Qt.DisplayRole, 0, 33],
                            FILESIZE_MB : [Qt.DisplayRole, 0, 33],
                            REEL        : [Qt.DisplayRole, 0, 33],
                            FPS         : [Qt.DisplayRole, 0, 33],
                            SENSORFPS   : [Qt.DisplayRole, 0, 33],
                            LENGTH      : [Qt.DisplayRole, 0, 33],
                            TC          : [Qt.DisplayRole, 0, 33],
                            BIT         : [Qt.DisplayRole, 0, 33],
                            ALPHA       : [Qt.DisplayRole, 0, 33],
                            COLORSPACE  : [Qt.DisplayRole, 0, 33],
                            GAMMA       : [Qt.DisplayRole, 0, 33],
                            AUDIOCH     : [Qt.DisplayRole, 0, 33],
                            AUDIOSRATE  : [Qt.DisplayRole, 0, 33],
                            AUDIOCODEC  : [Qt.DisplayRole, 0, 33],
                            AUDIOBRATE  : [Qt.DisplayRole, 0, 33],
                            CREATETIME  : [Qt.DisplayRole, 0, 33],
                            FULLPATH    : [Qt.DisplayRole, 0, 33],
                            RELPATH     : [Qt.DisplayRole, 0, 33],
                            CHECKSUM    : [Qt.DisplayRole, 0, 33],
                            CHECKSUM_XXHASH : [Qt.DisplayRole, 0, 33],
                            CHECKSUM_MD5 : [Qt.DisplayRole, 0, 33],
                            CHECKSUM_SHA1 : [Qt.DisplayRole, 0, 33],
                            EXINFO      : [Qt.DisplayRole, 0, 33],
    }

    def_thumb_group = [THUMB_S,THUMB_C,THUMB_E]
    def_checksum_group = [CHECK_ALGO_MD5,CHECK_ALGO_SHA1,CHECK_ALGO_XXHASH]

    CORP_INFO = 'LespaceVision'
    Logdir = "Log"
    DebugDir = "Debug"

    msgBox = ""

    # OPT VALUE
    OPT_COLUMNLIST = 'SELECTCOLUMNS'
    OPT_THUMB_X = "THUMB_X"
    OPT_THUMB_Y = "THUMB_Y"
    OPT_THUMB_BRIGHT = "THUMB_BRIGHTNESS"
    OPT_THUMB_OFF_S = "THUMB_OFF_S"
    OPT_THUMB_OFF_C = "THUMB_OFF_C"
    OPT_THUMB_OFF_E = "THUMB_OFF_E"
    OPT_DISABLESEQ = "DISABLE_SEQ"
    OPT_STAFPS = "STA_FPS"
    OPT_CHECK_ALGO = "CHECK_ALGO"
    OPT_EYECATCH  = "EYECATCH_PATH"
    OPT_XLSXOUTTYPE = "XLSX_OTYPE"
    OPT_XLSXMAXROWS  = "XLSX_ROWS"
    OPT_LCID = "LCID"

    # OPT DEFAULT

    THUMB_DEFAULT_X = 176 # Thumbnail X default(16:9)
    THUMB_DEFAULT_Y = 99  # Thumbnail Y default(16:9)
    THUMB_DEFALUT_BRIGHT = 1.0
    THUMB_DEFAULT_OFF = 0.0
    THUMB_DEFAULT_OFF_E = 0.0/-1 # for "-0.0"
    DISABLESEQ_DEFAULT = False
    STAFPS_DEFAULT = 30.0
    XLSXOUTTYPE_DEFAULT = 2 # 0=book,1=sheet,2=all
    XLSXMAXROWS_DEFAULT = 100
    LCID_DEFAULT = int(QtCore.QLocale.system().language())

    def __init__(self,app):
        super(MainWindow, self).__init__()

        self.framegrab = FrameGrabber(self)
        self.selectedframe = None

        self.shot = ShotList(self,framegrab=self.framegrab)
        self.dochome = os.path.join(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation), self.APPNAME)

        self.shot.setdochome(self.dochome)

        if not os.path.exists(self.dochome):
            os.mkdir(self.dochome)

        if not os.path.exists(os.path.join(self.dochome,self.Logdir)):
            os.mkdir(os.path.join(self.dochome,self.Logdir))

        self.columnlist = []
        self.thumbnail_x = 0
        self.thumbnail_y = 0
        self.thumbnail_bright = 1.0
        self.startoffset = 0.0
        self.centeroffset = 0.0
        self.endoffset = 0.0
        self.stafps = 0.0
        self.disableseq = None

        self.checksumalgo = self.CHECK_ALGO_XXHASH
        self.eyecatch = ""
        self.xlsxmaxrows = 0
        self.lcid = 0

        self.finderpath = None
        self.previewitem = None

        self.__readsettings()

        if(self.lcid == int(QtCore.QLocale.Japanese)):
            translator = QtCore.QTranslator()
            translator.load(":/qm/ShotList_ja_JP.qm")
            app.installTranslator(translator)

        self.setupUi(self)

        self.mainToolBar.hide()

        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setWindowTitle(self.APPNAME)
        self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)

        self.timerid = 0
        self.dot_count = 0
        self.status_label = StatusLabel("")
        self.main_processing = False
        self.haserror = False

        QtCore.QCoreApplication.setOrganizationName(self.CORP_INFO)

        verstr = "{0} v{1}".format(self.APPNAME,self.__version__)
        self.setWindowTitle(verstr)

        QtCore.QCoreApplication.setApplicationName(self.APPNAME)



        # make temporary directory(PySide2 bug? https://bugreports.qt.io/browse/PYSIDE-884
        tempdir = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
        tempdir = os.path.join(tempdir,self.APPID)
        if not os.path.isdir(tempdir):
            os.mkdir(tempdir)

        self.__initEv()

        self.lineEdit_SourceDir.setPlaceholderText(self.tr("input Folder path by D&D or src dialog"))

    def __initEv(self):

        self.tableWidget_shotlist.setRowCount(0)
        self.tableWidget_shotlist.setColumnCount(len(self.columnlist))
        self.tableWidget_shotlist.setHorizontalHeaderLabels(self.columnlist)

        self.statusBar.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.setAcceptDrops(True)
        self.lineEdit_SourceDir.setAcceptDrops(False)

        self.tableWidget_shotlist.setShowGrid(True)
        self.tableWidget_shotlist.setStyleSheet("QTableWidget::item { padding: 0px }")

        self.tableWidget_shotlist.setMouseTracking(True)
        self.tableWidget_shotlist.cellEntered.connect(self.cell_entered)

        self.pushButton_xlsout.clicked.connect(self.xlsout_clicked)
        self.pushButton_Input.clicked.connect(self.input_clicked)
        self.pushButton_import.clicked.connect(self.import_clicked)
        self.pushButton_shotclear.clicked.connect(self.shotclear_clicked)
        self.pushButton_reindex.clicked.connect(self.reindex_clicked)

        self.shot.finished.connect(self.finishThread)

        self.tableWidget_shotlist.itemClicked.connect(self.item_clicked)
        self.tableWidget_shotlist.itemDoubleClicked.connect(self.item_doubleclicked)
        self.tableWidget_shotlist.customContextMenuRequested.connect(self.__menu_opened)

        # mainSettings connect
        self.settingdialog = mainSettingDialog(parent=self)
        self.actionSettings.triggered.connect(self.__mainsetting_triggered)

        # about connect
        self.aboutdialog = aboutDialog(parent=self)
        self.actionAbout_ShotList.triggered.connect(self.__about_triggered)

        #Thumbnail menu and actions
        self.thumb_menu = QtWidgets.QMenu()
        self.action_preview = self.thumb_menu.addAction(self.tr("Select Thumbnail(preview)"))
        self.action_finder =  self.thumb_menu.addAction(self.tr("Open with Finder"))
        self.action_reindex = self.thumb_menu.addAction(self.tr("Reassign 'No.'"))

        self.showerrror_area(False)
        self.pushButton_reindex.setVisible(False)

        self.dummylabel = QtWidgets.QLabel("    ")

        self.prog_hlay = QtWidgets.QHBoxLayout(self.progressBar_import)
        self.prog_hlay.addWidget(self.status_label)
        self.prog_hlay.setContentsMargins(0,0,0,0)
        self.progressBar_import.setAlignment(QtCore.Qt.AlignLeft)
        self.statusBar.addPermanentWidget(self.dummylabel)
        self.statusBar.addPermanentWidget(self.progressBar_import,2)

        self.progressBar_import.setStyleSheet("QProgressBar::chunk {background-color: paleturquoise;}")
        self.progressBar_import.setTextVisible(False)

        return

    def __readsettings(self):

        self.cfg = QSettings(self.dochome + "/" + self.APPNAME + ".ini",QSettings.IniFormat)

        default_columns = self.def_columnlist[:]
        default_columns.remove(self.THUMB_S)
        default_columns.remove(self.THUMB_E)
        default_columns.remove(self.CHECKSUM)
        default_columns.remove(self.FILESIZE_MB)
        default_columns.remove(self.SENSORFPS)

        self.columnlist = self.cfg.value(self.OPT_COLUMNLIST,default_columns)

        self.thumbnail_x = int(self.cfg.value(self.OPT_THUMB_X,self.THUMB_DEFAULT_X))
        self.thumbnail_y = int(self.cfg.value(self.OPT_THUMB_Y,self.THUMB_DEFAULT_Y))
        self.thumbnail_bright = float(self.cfg.value(self.OPT_THUMB_BRIGHT,self.THUMB_DEFALUT_BRIGHT))
        self.startoffset = float(self.cfg.value(self.OPT_THUMB_OFF_S,self.THUMB_DEFAULT_OFF))
        self.centeroffset = float(self.cfg.value(self.OPT_THUMB_OFF_C, self.THUMB_DEFAULT_OFF))
        self.endoffset = float(self.cfg.value(self.OPT_THUMB_OFF_E, self.THUMB_DEFAULT_OFF_E))
        self.disableseq = self.cfg.value(self.OPT_DISABLESEQ,self.DISABLESEQ_DEFAULT)
        self.stafps = float(self.cfg.value(self.OPT_STAFPS,self.STAFPS_DEFAULT))
        self.checksumalgo = str(self.cfg.value(self.OPT_CHECK_ALGO,self.CHECK_ALGO_XXHASH))
        self.eyecatch = str(self.cfg.value(self.OPT_EYECATCH,""))
        self.xlsxouttype = int(self.cfg.value(self.OPT_XLSXOUTTYPE,self.XLSXOUTTYPE_DEFAULT))
        self.xlsxmaxrows = int(self.cfg.value(self.OPT_XLSXMAXROWS,self.XLSXMAXROWS_DEFAULT))
        self.lcid = int(self.cfg.value(self.OPT_LCID,self.LCID_DEFAULT))

        return

    def __writesettings(self):
        pass

    def __makelistfromqcombo(self,combobox):
        itemlist = []
        for i in range(combobox.count()):
            itemlist.append(combobox.itemText(i))
        itemlist.reverse()
        return itemlist

    def input_clicked(self):

        dir_path = QFileDialog.getExistingDirectory(self)

        if not dir_path:
            return
        else:
            self.lineEdit_SourceDir.setText(dir_path)

        return

    def import_clicked(self):

        if self.shot.isRunning():
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.setText(self.tr("Cancel import?"))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            self.shot.reqsuspend(True)
            if (msgBox.exec_() == QtWidgets.QMessageBox.Yes):
                self.shot.reqcancel(True)
            self.shot.reqsuspend(False)
            return
        elif self.main_processing:
            self.main_processing = False
            return

        ipath = self.lineEdit_SourceDir.text()

        if not ipath or not os.path.isdir(ipath):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.setText(self.tr("Please input folder path."))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()
            return

        self.textEdit_Result.clear()
        self.showerrror_area(False)

        self.tableWidget_shotlist.setSortingEnabled(False)
        self.tableWidget_shotlist.clearContents()
        self.tableWidget_shotlist.setColumnCount(len(self.columnlist))
        self.tableWidget_shotlist.setHorizontalHeaderLabels(self.columnlist)
        self.checkedcount = 0
        self.shot.reset()

        self.__setEnabled(False)
        self.pushButton_xlsout.setEnabled(False)

        self.shot.setOpt(self.shot.RUNMODE, self.shot.RUNMODE_IMPORT_IMAGES)
        self.shot.setOpt(self.shot.INPUT_PATH,ipath)

        self.beginTimer()
        self.haserror = False
        self.shot.start()
        self.progressBar_import.setStyleSheet("QProgressBar::chunk {background-color: paleturquoise;}")
        self.pushButton_import.setText(self.tr("Cancel.."))

    def xlsout_clicked(self):

        if self.tableWidget_shotlist.rowCount() == 0:
            return

        if self.shot.isRunning():
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.setWindowIcon(QtGui.QIcon(":/ico/" + self.APPNAME + ".ico"))
            msgBox.setText(self.tr("Cancel xlsxout?"))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            self.shot.reqsuspend(True)
            if (msgBox.exec_() == QtWidgets.QMessageBox.Yes):
                self.shot.reqcancel(True)
            self.shot.reqsuspend(False)
            return

        suffix_name = ""
        deskpath = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        writablepath = deskpath + os.sep

        if self.shot.optdict[self.shot.INPUT_PATH]:
            # print(os.path.split(self.shot.optdict[self.shot.INPUT_PATH])[1])
            suffix_name = os.path.split(self.shot.optdict[self.shot.INPUT_PATH])[1] + "_"

        # call multi xlsx files output
        if self.xlsxouttype == 0:
            dstpaths = []
            # prepare "all" xlsx filename
            # damn sandbox file output security....

            # defaultfilename = suffix_name + ".xlsx"
            rowcount = self.tableWidget_shotlist.rowCount()
            prev_index = 1
            if rowcount < self.xlsxmaxrows:
                next_index = rowcount
            else:
                next_index = self.xlsxmaxrows

            if rowcount % self.xlsxmaxrows == 0:
                total_fileno = rowcount / self.xlsxmaxrows
            else:
                total_fileno = math.ceil(rowcount / self.xlsxmaxrows)
            cur_fileno = 1
            for i in range(rowcount):

                if i != 0 and (i + 1)  % self.xlsxmaxrows == 0:
                    filename = suffix_name + "{0}_{1}".format(prev_index,next_index) + ".xlsx"
                    writablepath = writablepath + filename
                    dstpath = QFileDialog.getSaveFileName(self,
                                                          self.tr("Save xlsx({0}/{1})").format(cur_fileno,total_fileno),
                                                          writablepath)[0]
                    if dstpath:
                        dstpaths.append(dstpath)
                    else:
                        return
                    cur_fileno += 1
                    prev_index = prev_index + self.xlsxmaxrows
                    if next_index + self.xlsxmaxrows < rowcount:
                        next_index = next_index + self.xlsxmaxrows
                    else:
                        next_index = rowcount

                    writablepath = os.path.split(dstpath)[0] + os.sep
                elif i == rowcount - 1:
                    filename = suffix_name + "{0}_{1}".format(prev_index, next_index) + ".xlsx"
                    writablepath = writablepath + filename
                    dstpath = QFileDialog.getSaveFileName(self,
                                                          self.tr("Save xlsx({0}/{1})").format(cur_fileno, total_fileno),
                                                          writablepath)[0]
                    if dstpath:
                        dstpaths.append(dstpath)
                    else:
                        return

        else:

            defaultfilename = suffix_name + ".xlsx"

            savedialog = QFileDialog()

            writablepath = writablepath + defaultfilename
            dstpaths = QFileDialog.getSaveFileName(self,self.tr("Save xlsx"),
                                                  writablepath)[0]
            # cancel
            if not dstpaths:
                return

        self.progressBar_import.setStyleSheet("QProgressBar::chunk {background-color: paleturquoise;}")

        self.__prepare_xlsxout(dstpaths)

        self.__setEnabled(False)
        self.pushButton_import.setEnabled(False)
        self.beginTimer()
        self.haserror = False
        self.shot.start()

        self.pushButton_xlsout.setText(self.tr("Cancel.."))

    def shotclear_clicked(self):

        self.textEdit_Result.clear()

    def reindex_clicked(self):
        if self.tableWidget_shotlist.rowCount() == 0:
            return
        elif self.shot.isRunning():
            return

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText(self.tr("'No.' columns value will reassign. Are you sure?"))
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if (msgBox.exec_() == QtWidgets.QMessageBox.No):
            return

        for j in range(self.tableWidget_shotlist.columnCount()):
            if self.tableWidget_shotlist.horizontalHeaderItem(j).text() == self.NO:
                for i in range(self.tableWidget_shotlist.rowCount()):
                    item = self.tableWidget_shotlist.takeItem(i,j)
                    item.setData(QtCore.Qt.DisplayRole, i + 1)
                    self.tableWidget_shotlist.setItem(i, j, item)
                    # print(item.data(QtCore.Qt.DisplayRole))

        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(self.tr("'No.' columns reassigned complete."))
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes)
        msgBox.exec_()

    def cell_entered(self,x,y):
        item = self.tableWidget_shotlist.item(x,y)
        datadict = item.data(Qt.UserRole)
        if datadict:
            self.finderpath = datadict[self.DIRPATH_HIDDEN]
            self.previewitem = item
        else:
            self.finderpath = None
            self.previewitem = None

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        url = event.mimeData().urls()[0]
        path = url.toLocalFile()

        if(path[-1:] == "/"):
            path = path[:-1]

        if not os.path.isdir(path):
            self.status_label.setText(self.tr("Error:path is file. Plz input folder. path={0}").format(path))
            return

        self.lineEdit_SourceDir.setText(path)

    def closeEvent(self,cevent):

        if not self.shot.isRunning() or self.shot.isFinished():
            cevent.accept()
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setWindowIcon(QtGui.QIcon(":/ico/" + self.APPNAME + ".ico"))
            msgBox.setText(self.tr("ShotList is running"))
            msgBox.setInformativeText(self.tr("Can't close ShotList while current task."))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()
            cevent.ignore()

    def timerEvent(self,tevent):
        if(tevent.timerId() == self.timerid and self.shot.message):
            self.progressBar_import.setMaximum(self.shot.totalseqno)
            self.progressBar_import.setValue(self.shot.currentseqno)

            replstr = self.shot.message
            dotstr = ""
            for i in range(0,self.dot_count):
                dotstr += "."

            self.status_label.setText(replstr + dotstr)


        self.dot_count += 1
        if(self.dot_count == 4):
            self.dot_count = 0
        # did not take Lock but maybe no problem.
        if len((self.shot.errmessages)):
            self.showerrror_area(True)
            self.progressBar_import.setStyleSheet("QProgressBar::chunk {background-color: orange;}")
            self.haserror = True
            for i in range(len(self.shot.errmessages)):
                self.textEdit_Result.append(self.shot.errmessages[i])
            self.shot.errmessages.clear()

    def beginTimer(self):
        self.timerid = QObject.startTimer(self,1000)

    # @QtCore.Slot()
    def stopTimer(self):
        self.status_label.clear()
        QObject.killTimer(self,self.timerid)

    @QtCore.Slot()
    def beginTimer(self):
        self.timerid = QObject.startTimer(self,1000)

    @QtCore.Slot()
    def stopTimer(self):
        QObject.killTimer(self,self.timerid)

    @QtCore.Slot(str)
    def finishThread(self):

        self.main_processing = True

        self.stopTimer()
        # Output error message when exists
        if len((self.shot.errmessages)):
            self.showerrror_area(True)

            for i in range(len(self.shot.errmessages)):
                self.textEdit_Result.append(self.shot.errmessages[i])

        # Import image
        if self.shot.optdict[self.shot.RUNMODE] == self.shot.RUNMODE_IMPORT_IMAGES:
            if self.shot.req_cancel:
                self.status_label.setText(self.tr("import canceled."))
                self.tableWidget_shotlist.clearContents()
                self.tableWidget_shotlist.setRowCount(0)
            else:

                if len(self.shot.inputresultlist):
                    self.__setrecord(self.shot.inputresultlist)
                    self.fitcolumns()
                else:
                    errstr = self.tr("No shot(s).")
                    self.textEdit_Result.append(errstr)
                    self.msgBox.setText(errstr)
                    self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
                    self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.msgBox.exec_()
                    self.label_preview.setText(self.tr("No shot(s)."))

                self.status_label.setText(self.tr("Import finished"))

                if self.haserror:
                    self.progressBar_import.setStyleSheet("QProgressBar::chunk {background-color: orange;}")
                else:
                    self.progressBar_import.setStyleSheet("QProgressBar::chunk {background-color: lightgreen;}")

        # xlsx output
        else:
            if self.shot.req_cancel:
                # xlsx output canceled.
                self.status_label.setText(self.tr("xlsx out canceled"))
            else:
                # xlsx output finished
                self.status_label.setText(self.tr("xlsx out finished"))
                self.textEdit_Result.append(self.tr("xlsx out finished. out path = {0}".format(self.shot.optdict[self.shot.OUTPUT_PATH])))
                self.msgBox.setText(self.tr("xlsx out finished."))
                if self.xlsxouttype == 0:
                    self.msgBox.setInformativeText(self.tr("xlsx out finished."))
                else:
                    self.msgBox.setInformativeText(self.tr("xlsx out finished. out path = {0}".format(self.shot.optdict[self.shot.OUTPUT_PATH])))
                self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
                self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msgBox.exec_()

            self.progressBar_import.setStyleSheet("QProgressBar::chunk {background-color: lightgreen;}")

        self.progressBar_import.setValue(self.progressBar_import.maximum())

        # enable mainwindows buttons.
        self.__setEnabled(True)
        self.pushButton_import.setEnabled(True)
        self.pushButton_xlsout.setEnabled(True)
        self.main_processing = False
        self.pushButton_import.setText(self.tr("Import"))
        self.pushButton_xlsout.setText(self.tr("xlsx output"))
        self.shot.reqsuspend(False)
        self.shot.reqcancel(False)
        self.msgBox.setInformativeText("")

    @QtCore.Slot()
    def item_clicked(self, item):
        pass

    @QtCore.Slot()
    def item_doubleclicked(self, item):

        columnname = self.tableWidget_shotlist.horizontalHeaderItem(item.column()).text()

        if(columnname in self.def_thumb_group):

            itemdict = self.tableWidget_shotlist.item(item.row(),item.column()).data(Qt.UserRole)

            ext = os.path.splitext(itemdict[self.FILENAME_HIDDEN])[1].lower()

            if ext in self.shot.SUPPORT_MOVIMAGES:
                # QtWidgets.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fullpath))
                fullpath = os.path.join(itemdict[self.DIRPATH_HIDDEN],itemdict[self.FILENAME_HIDDEN])
                previewdialog = VideoPlayerDialog(parent=self,path=fullpath)

                if columnname == self.THUMB_C:
                    previewdialog.set_slider(1)
                elif columnname == self.THUMB_E:
                    previewdialog.set_slider(2)
                else:
                    pass

            elif ext in self.shot.SUPPORT_STAIMAGES:

                filelist = []

                # save memory usage. reconstruct fullpath...
                for filename in itemdict[self.SEQPATH_HIDDEN]:
                    filelist.append(os.path.join(itemdict[self.DIRPATH_HIDDEN],filename))

                seq = pyseq.Sequence(filelist)

                previewdialog = SequencePlayerDialog(parent=self, seq=seq)
                end = seq.end()
                start = seq.start()
                length = seq.end() - seq.start()

                if columnname == self.THUMB_S:
                    previewdialog.slider_changed(start)
                elif columnname == self.THUMB_C:
                    previewdialog.slider_changed(start + (length / 2))
                elif columnname == self.THUMB_E:
                    previewdialog.slider_changed(end)
                else:
                    pass
            else:
                return

            if previewdialog.exec_() == QtWidgets.QDialog.Accepted:
                xy = self.shot.resize_xandy(self.selectedframe.width(),self.selectedframe.height())
                self.selectedframe = self.selectedframe.scaled(xy[0],xy[1],
                                                               Qt.KeepAspectRatio,Qt.SmoothTransformation)
                item.setData(QtCore.Qt.DecorationRole,self.selectedframe)

    @QtCore.Slot()
    def __mainsetting_triggered(self):

        if self.settingdialog.exec_() == QtWidgets.QDialog.Accepted:
            self.fitcolumns()

    @QtCore.Slot()
    def __about_triggered(self):
        self.aboutdialog.exec_()

    def __menu_opened(self,position):

        action = self.thumb_menu.exec_(self.tableWidget_shotlist.mapToGlobal(position))

        if action == self.action_finder:
            # self.finderpath set by cell_entered SLOT
            if self.finderpath:
                QDesktopServices.openUrl("file:///" + self.finderpath)
        elif action == self.action_preview:
            if self.previewitem:
                self.item_doubleclicked(self.previewitem)
        elif action == self.action_reindex:
            self.reindex_clicked()
        else:
            pass

    def __setrecord(self,resultlist):

        self.tableWidget_shotlist.setRowCount(len(resultlist))

        for i,rec in enumerate(resultlist):

            self.status_label.setText(self.tr("Setting Rows({0}/{1})").format(i,len(resultlist)))

            # check cancel
            if self.shot.req_cancel or self.main_processing is False:
                self.status_label.setText(self.tr("import canceled."))
                self.tableWidget_shotlist.clearContents()
                self.tableWidget_shotlist.setRowCount(0)
                return False
            else:
                self.status_label.setText(self.tr("set record {0}/{1}".format(i,len(resultlist))))

            for j in range(self.tableWidget_shotlist.columnCount()):
                columnname = self.tableWidget_shotlist.horizontalHeaderItem(j).text()
                item = QtWidgets.QTableWidgetItem()
                declist = self.def_columnpropdict[columnname]
                if declist[1]:
                    if columnname in self.def_thumb_group:
                        if isinstance(rec[columnname],str):
                            item.setText(rec[columnname])
                        else:
                            qimage = QtGui.QPixmap.fromImage(rec[columnname])
                            item.setData(declist[0],qimage)
                            self.tableWidget_shotlist.setRowHeight(i,qimage.height() + 5)

                            itemdict = {}
                            itemdict[self.DIRPATH_HIDDEN] = rec[self.DIRPATH_HIDDEN]
                            itemdict[self.FILENAME_HIDDEN] = rec[self.FILENAME_HIDDEN]


                            if rec[self.SEQPATH_HIDDEN]:
                                itemdict[self.SEQPATH_HIDDEN] = rec[self.SEQPATH_HIDDEN]
                                if columnname == self.THUMB_S and rec[self.SEQ_HIDDEN_S]:
                                    item.setData(self.SeqRole,rec[self.SEQ_HIDDEN_S])
                                elif columnname == self.THUMB_C and rec[self.SEQ_HIDDEN_C]:
                                    item.setData(self.SeqRole,rec[self.SEQ_HIDDEN_C])
                                elif columnname == self.THUMB_E and rec[self.SEQ_HIDDEN_E]:
                                    item.setData(self.SeqRole,rec[self.SEQ_HIDDEN_E])
                                else:
                                    pass
                            else:
                                pass

                            item.setData(Qt.UserRole, itemdict)

                    else:
                        item.setData(declist[0],rec[columnname])

                else:
                    item.setText(str(rec[columnname]))

                if declist[2] == 33:
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                elif declist[2] == 35:
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsEnabled)
                else:
                    pass
                # item.setFlags(declist[2])
                self.tableWidget_shotlist.setItem(i,j,item)

        for j in range(self.tableWidget_shotlist.columnCount()):
            if self.tableWidget_shotlist.horizontalHeaderItem(j).text() == self.CHECKSUM:
                checksum_item = self.tableWidget_shotlist.horizontalHeaderItem(j)
                checksum_item.setText(checksum_item.text() + self.checksumalgo)

        self.label_preview.setText(self.tr("{0} shots total".format(len(resultlist))))
        return True

    def __setEnabled(self,req_bool):
        self.pushButton_Input.setEnabled(req_bool)
        self.tableWidget_shotlist.setEnabled(req_bool)
        self.pushButton_reindex.setEnabled(req_bool)

    def __setColortoRow(self,table,rowIndex,color):
        for j in range(table.columnCount()):
            table.item(rowIndex,j).setBackground(color)

    # output process running on execute thread,so prepare for xlsx output.
    def __prepare_xlsxout(self,outpaths):

        # We do what we can only operate on the main thread.
        # Throw real out to a thread
        if not self.tableWidget_shotlist.rowCount:
            return

        tablelist = []
        for i in range(self.tableWidget_shotlist.rowCount()):

            self.status_label.setText(self.tr("xlsx preparing Rows({0}/{1})").format(i, self.tableWidget_shotlist.rowCount()))
            row_list_rec = []

            for j in range(self.tableWidget_shotlist.columnCount()):

                if self.tableWidget_shotlist.horizontalHeaderItem(j).text() in self.def_thumb_group\
                   and self.tableWidget_shotlist.item(i,j).data(QtCore.Qt.DecorationRole):
                    row_list_rec.append(self.tableWidget_shotlist.item(i, j).data(QtCore.Qt.DecorationRole))
                else:
                    row_list_rec.append(self.tableWidget_shotlist.item(i, j).text())

            tablelist.append(row_list_rec)

        # checksum type string add.
        for i,columnname in enumerate(self.columnlist):
            if columnname == self.CHECKSUM:
                self.columnlist[i] = self.columnlist[i] + self.checksumalgo

        self.shot.setOpt(self.shot.OUTPUT_COLUMNS, self.columnlist)
        self.shot.setOpt(self.shot.OUTPUT_ROWS,tablelist)

        # xlsx output path set
        self.shot.setOpt(self.shot.RUNMODE,self.shot.RUNMODE_OUT_XLSX)
        self.shot.setOpt(self.shot.OPT_XLSXOUTTYPE, self.xlsxouttype)
        self.shot.setOpt(self.shot.OPT_XLSXMAXROWS, self.xlsxmaxrows)
        self.shot.setOpt(self.shot.OUTPUT_PATH,outpaths)

    def fitcolumns(self):

        self.tableWidget_shotlist.resizeColumnToContents(0)
        self.tableWidget_shotlist.resizeColumnsToContents()
        self.tableWidget_shotlist.setSortingEnabled(True)
        self.tableWidget_shotlist.sortByColumn(0,QtCore.Qt.AscendingOrder)
        self.tableWidget_shotlist.clearSelection()
        #self.tableWidget_shotlist.resizeRowsToContents()

    def showerrror_area(self,isvisible):
        self.label_log.setVisible(isvisible)
        self.textEdit_Result.setVisible(isvisible)
        self.pushButton_shotclear.setVisible(isvisible)


def strtofloat(num_str, default=0):
    try:
        floatvalue = float(num_str)
    except ValueError:
        return default
    return floatvalue
