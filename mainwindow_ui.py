# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow_ui.ui',
# licensing of 'mainwindow_ui.ui' applies.
#
# Created: Sun Jun  2 18:59:42 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(844, 697)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_import = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_import.setFont(font)
        self.pushButton_import.setObjectName("pushButton_import")
        self.gridLayout.addWidget(self.pushButton_import, 0, 0, 1, 1)
        self._editsort = QtWidgets.QLabel(self.centralWidget)
        self._editsort.setObjectName("_editsort")
        self.gridLayout.addWidget(self._editsort, 1, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.tableWidget_shotlist = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget_shotlist.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_shotlist.sizePolicy().hasHeightForWidth())
        self.tableWidget_shotlist.setSizePolicy(sizePolicy)
        self.tableWidget_shotlist.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        self.tableWidget_shotlist.setFont(font)
        self.tableWidget_shotlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget_shotlist.setInputMethodHints(QtCore.Qt.ImhNone)
        self.tableWidget_shotlist.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget_shotlist.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_shotlist.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_shotlist.setAutoScroll(False)
        self.tableWidget_shotlist.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.SelectedClicked)
        self.tableWidget_shotlist.setTabKeyNavigation(False)
        self.tableWidget_shotlist.setProperty("showDropIndicator", False)
        self.tableWidget_shotlist.setDragDropOverwriteMode(False)
        self.tableWidget_shotlist.setAlternatingRowColors(True)
        self.tableWidget_shotlist.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tableWidget_shotlist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableWidget_shotlist.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidget_shotlist.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget_shotlist.setShowGrid(True)
        self.tableWidget_shotlist.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget_shotlist.setWordWrap(True)
        self.tableWidget_shotlist.setCornerButtonEnabled(True)
        self.tableWidget_shotlist.setRowCount(101)
        self.tableWidget_shotlist.setColumnCount(38)
        self.tableWidget_shotlist.setObjectName("tableWidget_shotlist")
        self.tableWidget_shotlist.setColumnCount(38)
        self.tableWidget_shotlist.setRowCount(101)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(21, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(22, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(23, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(24, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(25, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(26, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setHorizontalHeaderItem(27, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget_shotlist.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setItem(1, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setItem(1, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setItem(1, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setItem(1, 8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setItem(1, 9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setItem(1, 11, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget_shotlist.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_shotlist.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget_shotlist.setItem(3, 0, item)
        self.tableWidget_shotlist.horizontalHeader().setVisible(True)
        self.tableWidget_shotlist.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget_shotlist.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_shotlist.horizontalHeader().setHighlightSections(True)
        self.tableWidget_shotlist.horizontalHeader().setMinimumSectionSize(30)
        self.tableWidget_shotlist.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_shotlist.verticalHeader().setVisible(False)
        self.tableWidget_shotlist.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget_shotlist.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget_shotlist.verticalHeader().setMinimumSectionSize(30)
        self.tableWidget_shotlist.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_4.addWidget(self.tableWidget_shotlist)
        self.label_preview = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_preview.sizePolicy().hasHeightForWidth())
        self.label_preview.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setWeight(75)
        font.setBold(True)
        self.label_preview.setFont(font)
        self.label_preview.setObjectName("label_preview")
        self.verticalLayout_4.addWidget(self.label_preview)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_xlsout = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_xlsout.setFont(font)
        self.pushButton_xlsout.setObjectName("pushButton_xlsout")
        self.horizontalLayout.addWidget(self.pushButton_xlsout)
        self.pushButton_reindex = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_reindex.setObjectName("pushButton_reindex")
        self.horizontalLayout.addWidget(self.pushButton_reindex)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.label_log = QtWidgets.QLabel(self.centralWidget)
        self.label_log.setObjectName("label_log")
        self.verticalLayout_4.addWidget(self.label_log)
        self.textEdit_Result = QtWidgets.QTextEdit(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_Result.sizePolicy().hasHeightForWidth())
        self.textEdit_Result.setSizePolicy(sizePolicy)
        self.textEdit_Result.setMinimumSize(QtCore.QSize(0, 120))
        self.textEdit_Result.setMaximumSize(QtCore.QSize(16777215, 240))
        self.textEdit_Result.setObjectName("textEdit_Result")
        self.verticalLayout_4.addWidget(self.textEdit_Result)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_shotclear = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_shotclear.setObjectName("pushButton_shotclear")
        self.horizontalLayout_2.addWidget(self.pushButton_shotclear)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.gridLayout_3.addLayout(self.verticalLayout_4, 1, 2, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_Input = QtWidgets.QPushButton(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Input.sizePolicy().hasHeightForWidth())
        self.pushButton_Input.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_Input.setFont(font)
        self.pushButton_Input.setObjectName("pushButton_Input")
        self.gridLayout_2.addWidget(self.pushButton_Input, 1, 0, 1, 1)
        self.lineEdit_SourceDir = QtWidgets.QLineEdit(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_SourceDir.sizePolicy().hasHeightForWidth())
        self.lineEdit_SourceDir.setSizePolicy(sizePolicy)
        self.lineEdit_SourceDir.setObjectName("lineEdit_SourceDir")
        self.gridLayout_2.addWidget(self.lineEdit_SourceDir, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 2)
        self.progressBar_import = QtWidgets.QProgressBar(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.progressBar_import.setFont(font)
        self.progressBar_import.setProperty("value", 0)
        self.progressBar_import.setObjectName("progressBar_import")
        self.gridLayout_3.addWidget(self.progressBar_import, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 844, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionAbout_ShotList = QtWidgets.QAction(MainWindow)
        self.actionAbout_ShotList.setMenuRole(QtWidgets.QAction.AboutRole)
        self.actionAbout_ShotList.setObjectName("actionAbout_ShotList")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.actionSettings.setObjectName("actionSettings")
        self.menuFile.addAction(self.actionAbout_ShotList)
        self.menuFile.addAction(self.actionSettings)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "ShotList", None, -1))
        self.pushButton_import.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Start import movie/still image from input folder.", None, -1))
        self.pushButton_import.setText(QtWidgets.QApplication.translate("MainWindow", "Import", None, -1))
        self._editsort.setText(QtWidgets.QApplication.translate("MainWindow", "EDIT / SORT", None, -1))
        self.tableWidget_shotlist.setToolTip(QtWidgets.QApplication.translate("MainWindow", "\"No\",\"Reel\",\"Scene\",\"Cut\",\"Take\",\"Comment\" is editable by double click.\n"
"Double click: Open preview and select thumbnail\n"
"Right-click -> Open in Finder: Open path in Finder\n"
"Reassign \"No\": In the display order of the current ShotList preview,\n"
"                          Resign \"No\" column from 1 to max rows no.\n"
"", None, -1))
        self.tableWidget_shotlist.setSortingEnabled(True)
        self.tableWidget_shotlist.verticalHeaderItem(0).setText(QtWidgets.QApplication.translate("MainWindow", "1", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("MainWindow", "No", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("MainWindow", "Thumbnail", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("MainWindow", "FileName", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(3).setText(QtWidgets.QApplication.translate("MainWindow", "Scene", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(4).setText(QtWidgets.QApplication.translate("MainWindow", "Cut", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(5).setText(QtWidgets.QApplication.translate("MainWindow", "Comment", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(6).setText(QtWidgets.QApplication.translate("MainWindow", "Container", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(7).setText(QtWidgets.QApplication.translate("MainWindow", "Codec\n"
"(Compress)", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(8).setText(QtWidgets.QApplication.translate("MainWindow", "PixSize", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(9).setText(QtWidgets.QApplication.translate("MainWindow", "filesize\n"
"(GB)", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(10).setText(QtWidgets.QApplication.translate("MainWindow", "Reel", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(11).setText(QtWidgets.QApplication.translate("MainWindow", "fps", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(12).setText(QtWidgets.QApplication.translate("MainWindow", "Length", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(13).setText(QtWidgets.QApplication.translate("MainWindow", "TC", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(14).setText(QtWidgets.QApplication.translate("MainWindow", "TC(SMPTE)", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(15).setText(QtWidgets.QApplication.translate("MainWindow", "bit", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(16).setText(QtWidgets.QApplication.translate("MainWindow", "alpha", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(17).setText(QtWidgets.QApplication.translate("MainWindow", "colorspace", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(18).setText(QtWidgets.QApplication.translate("MainWindow", "gamma", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(19).setText(QtWidgets.QApplication.translate("MainWindow", "Audio ch", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(20).setText(QtWidgets.QApplication.translate("MainWindow", "Audio rate", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(21).setText(QtWidgets.QApplication.translate("MainWindow", "Audio codec", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(22).setText(QtWidgets.QApplication.translate("MainWindow", "Audio bitrate", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(23).setText(QtWidgets.QApplication.translate("MainWindow", "CreateTime", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(24).setText(QtWidgets.QApplication.translate("MainWindow", "fullpath", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(25).setText(QtWidgets.QApplication.translate("MainWindow", "relpath", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(26).setText(QtWidgets.QApplication.translate("MainWindow", "checksum", None, -1))
        self.tableWidget_shotlist.horizontalHeaderItem(27).setText(QtWidgets.QApplication.translate("MainWindow", "Exinfo", None, -1))
        __sortingEnabled = self.tableWidget_shotlist.isSortingEnabled()
        self.tableWidget_shotlist.setSortingEnabled(False)
        self.tableWidget_shotlist.setSortingEnabled(__sortingEnabled)
        self.label_preview.setText(QtWidgets.QApplication.translate("MainWindow", "0 shots total", None, -1))
        self.pushButton_xlsout.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Output xlsx file with current ShotList preview.", None, -1))
        self.pushButton_xlsout.setText(QtWidgets.QApplication.translate("MainWindow", "xlsx output", None, -1))
        self.pushButton_reindex.setToolTip(QtWidgets.QApplication.translate("MainWindow", "In the display order of the current ShotListpreview,\n"
"Reassign \"No\" column from 1 to max rows.", None, -1))
        self.pushButton_reindex.setText(QtWidgets.QApplication.translate("MainWindow", "Reassign No", None, -1))
        self.label_log.setText(QtWidgets.QApplication.translate("MainWindow", "Error log:", None, -1))
        self.textEdit_Result.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Show running processes.\n"
"When an error occurs, the cause is displayed, so please use it as a hint to solve the problem.", None, -1))
        self.textEdit_Result.setHtml(QtWidgets.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, -1))
        self.pushButton_shotclear.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Clear current information log.", None, -1))
        self.pushButton_shotclear.setText(QtWidgets.QApplication.translate("MainWindow", "clear Error log", None, -1))
        self.pushButton_Input.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Select import folder(open Folder Dialog)", None, -1))
        self.pushButton_Input.setText(QtWidgets.QApplication.translate("MainWindow", "Select Folder..", None, -1))
        self.lineEdit_SourceDir.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Input folder path(D&D OK)", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.actionAbout_ShotList.setText(QtWidgets.QApplication.translate("MainWindow", "About ShotList", None, -1))
        self.actionSettings.setText(QtWidgets.QApplication.translate("MainWindow", "Settings", None, -1))

