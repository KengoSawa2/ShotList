# -*- coding: utf-8 -*-

from __future__ import print_function


from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore

from PySide2.QtCore import Qt
from PySide2.QtCore import Signal
from DisplayWidget import DisplayWidget

from SequenceGrabber import SequenceGrabber

import sys
import math
import pyseq

class SequencePlayerDialog(QtWidgets.QDialog):

    request_time = Signal(object)

    load_file = Signal(object)

    def __init__(self, parent=None,seq=None):
        super(SequencePlayerDialog, self).__init__(parent)

        self.mw = parent
        self.seq = seq
        self.maximum = len(seq) - 1
        self.captured = False

        self.display = DisplayWidget()
        self.timeline = QtWidgets.QScrollBar(Qt.Horizontal)

        self.seq_grabber = SequenceGrabber(mw=self.mw,seq=self.seq)

        self.frame_capture = QtWidgets.QPushButton("Set thumbnail")
        # self.frame_capture.setEnabled(False)
        self.frame_capture.setFixedWidth(120)
        self.frame_capture.clicked.connect(self.frame_captured)

        self.frame_control = QtWidgets.QSpinBox()
        self.frame_control.setFixedWidth(100)

        self.timeline.valueChanged.connect(self.slider_changed)
        self.frame_control.valueChanged.connect(self.frame_changed)

        self.request_time.connect(self.seq_grabber.request_time)
        # self.load_file.connect(self.seq_grabber.set_container)

        self.seq_grabber.frame_ready.connect(self.display.setPixmap)
        # self.seq_grabber.update_frame_range.connect(self.set_frame_range)

        self.frame_grabber_thread = QtCore.QThread()

        self.seq_grabber.moveToThread(self.frame_grabber_thread)
        self.frame_grabber_thread.start()

        control_layout = QtWidgets.QHBoxLayout()
        control_layout.addWidget(self.frame_control)
        control_layout.addWidget(self.timeline)
        control_layout.addWidget(self.frame_capture)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(control_layout)
        self.setLayout(layout)
        self.setAcceptDrops(False)
        self.setWindowTitle(self.tr("Sequence Preview"))
        self.set_frame_range()

    @QtCore.Slot(object, object)
    def set_frame_range(self):

        self.timeline.setMinimum(self.seq.start())
        self.timeline.setMaximum(self.seq.end())
        self.frame_control.setMinimum(self.seq.start())
        self.frame_control.setMaximum(self.seq.end())
        self.frame_control.setSingleStep(1)
        self.maximum = self.seq.end()

    def slider_changed(self, value):
        self.frame_changed(value)

    def frame_changed(self, value):
        self.timeline.blockSignals(True)
        self.frame_control.blockSignals(True)

        self.timeline.setValue(value)
        self.frame_control.setValue(value)

        self.timeline.blockSignals(False)
        self.frame_control.blockSignals(False)

        self.seq_grabber.active_time = value

        self.request_time.emit(value)

    def frame_captured(self):
        if self.display.pixmap:
            self.mw.selectedframe = self.display.pixmap
            self.captured = True
            self.accept()
            self.close()

    def keyPressEvent(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        if event.key() in (Qt.Key_Right, Qt.Key_Left):
            direction = 1
            if event.key() == Qt.Key_Left:
                direction = -1

            if modifiers == Qt.ShiftModifier:
                direction *= 10
            nextdirection = self.frame_control.value() + direction
            if nextdirection < self.timeline.minimum() or nextdirection > self.timeline.maximum():
                super(SequencePlayerDialog, self).keyPressEvent(event)
            else:
                self.frame_changed(nextdirection)
        else:
            super(SequencePlayerDialog, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        # clear focus of spinbox
        focused_widget = QtWidgets.QApplication.focusWidget()
        if focused_widget:
            focused_widget.clearFocus()

        super(SequencePlayerDialog, self).mousePressEvent(event)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):

        mime = event.mimeData()
        event.accept()

        if mime.hasUrls():
            path = str(mime.urls()[0].path())
            self.set_file(path)
    def closeEvent(self, event):

        self.seq_grabber.active_time = -1
        self.frame_grabber_thread.quit()
        self.frame_grabber_thread.wait()

        event.accept()
        if self.mw.selectedframe and self.captured:
            self.accept()
        else:
            self.reject()
