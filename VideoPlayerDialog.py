from __future__ import print_function


from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from PySide2.QtCore import Qt
from PySide2.QtCore import Signal
from DisplayWidget import DisplayWidget

from FrameGrabber import FrameGrabber

import sys
import av

class VideoPlayerDialog(QtWidgets.QDialog):

    request_time = Signal(object)

    load_file = Signal(object)

    def __init__(self, parent=None,path=None):
        super(VideoPlayerDialog, self).__init__(parent)

        self.mw = parent
        self.rate = None
        self.maximum = 0
        self.dispbefore_seek = 0
        self.captured = False

        self.display = DisplayWidget()
        self.timeline = QtWidgets.QScrollBar(Qt.Horizontal)
        self.timeline_base = 100000

        self.frame_grabber = FrameGrabber(mw=self.mw)

        self.frame_capture = QtWidgets.QPushButton("Set thumbnail")
        # self.frame_capture.setEnabled(False)
        self.frame_capture.setFixedWidth(120)
        self.frame_capture.clicked.connect(self.frame_captured)

        self.frame_control = QtWidgets.QDoubleSpinBox()
        self.frame_control.setFixedWidth(100)


        self.timeline.valueChanged.connect(self.slider_changed)
        self.frame_control.valueChanged.connect(self.frame_changed)

        self.request_time.connect(self.frame_grabber.request_time)
        self.load_file.connect(self.frame_grabber.set_container)

        self.frame_grabber.frame_ready.connect(self.display.setPixmap)
        self.frame_grabber.update_frame_range.connect(self.set_frame_range)

        self.frame_grabber_thread = QtCore.QThread()

        self.frame_grabber.moveToThread(self.frame_grabber_thread)
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
        self.setWindowTitle(self.tr("Movie Preview"))
        if path:
            container = None
            try:
                container = av.open(path, 'r',metadata_encoding='utf-8',metadata_errors='ignore')
            except Exception as ex:
                exstr = 'av.open() exception:' + path + " " + str(ex)
                print(exstr)
                # print mainwindow?
                return self.Rejected
            self.set_file(container)

    def set_file(self, path):
        #self.seq_grabber.set_file(path)
        self.load_file.emit(path)
        self.frame_changed(0)

    def set_slider(self,req):
        self.dispbefore_seek = req

    @QtCore.Slot(object, object)
    def set_frame_range(self, maximum, rate):

        self.timeline.setMaximum(int(maximum * self.timeline_base))

        self.frame_control.setMaximum(maximum)
        self.frame_control.setSingleStep(1 / rate)
        #self.timeline.setSingleStep( int(AV_TIME_BASE * 1/rate))
        self.maximum = maximum
        self.rate = rate
        if self.dispbefore_seek == 1:
            self.frame_changed(self.maximum / 2)
        elif self.dispbefore_seek == 2:
            self.frame_changed(self.maximum)
        else: #start
            pass

    def slider_changed(self, value):
        self.frame_changed(value * 1.0 / float(self.timeline_base))

    def frame_changed(self, value):
        self.timeline.blockSignals(True)
        self.frame_control.blockSignals(True)

        self.timeline.setValue(int(value * self.timeline_base))
        self.frame_control.setValue(value)

        self.timeline.blockSignals(False)
        self.frame_control.blockSignals(False)

        #self.display.current_index = value
        self.frame_grabber.active_time = value

        self.request_time.emit(value)

    def frame_captured(self):
        if self.display.pixmap:
            self.mw.selectedframe = self.display.pixmap
            self.captured = True
            self.accept()
            self.close()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Right, Qt.Key_Left):
            direction = 1
            if event.key() == Qt.Key_Left:
                direction = -1

            if event.modifiers() == Qt.ShiftModifier:
                direction *= 10

            direction = direction * 1 / self.rate

            self.frame_changed(self.frame_control.value() + direction)

        else:
            super(VideoPlayerDialog, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        # clear focus of spinbox
        focused_widget = QtWidgets.QApplication.focusWidget()
        if focused_widget:
            focused_widget.clearFocus()

        super(VideoPlayerDialog, self).mousePressEvent(event)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):

        mime = event.mimeData()
        event.accept()

        if mime.hasUrls():
            path = str(mime.urls()[0].path())
            self.set_file(path)
    def closeEvent(self, event):

        self.frame_grabber.active_time = -1
        self.frame_grabber_thread.quit()
        self.frame_grabber_thread.wait()

        # for key, value in sorted(self.seq_grabber.pts_map.items()):
        #     print(key, '=', value)
        event.accept()
        if self.mw.selectedframe and self.captured:
            self.accept()
        else:
            self.reject()
