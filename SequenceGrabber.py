# -*- coding: utf-8 -*-

# FrameGrabber class referece from Pyav/Example/second_seek_example.py

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtCore import Signal
from PySide2.QtCore import QStandardPaths
from PySide2.QtGui import QImage

import sys
import av
import os

import OpenImageIO as oiio
from OpenImageIO import ImageBuf

from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageEnhance
from PIL import Image, ImageDraw, ImageFont

AV_TIME_BASE = 1000000

class SequenceGrabber(QtCore.QObject):

    frame_ready = Signal(object, object)
    # update_frame_range = Signal()



    def __init__(self, parent=None,mw=None,seq=None,refimage=None):
        super(SequenceGrabber, self).__init__(parent)
        self.mw = mw
        self.seq = seq
        self.frame = None
        self.active_time = None

        try:
            ibuf = ImageBuf(self.seq[0].path)
        except Exception as ex:
            print(ex)
            return
        spec = ibuf.spec()

        im = Image.new("RGB", (spec.width, spec.height), (0, 0, 0))
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 48)
        draw.text((spec.width / 3,spec.height / 2),"No Image",font=font)
        self.blank_qimage = ImageQt(im)

        wksavepath = "/tmp"
        wksavepath = wksavepath + "/sequencemissing.jpg".format(self.mw.APPID)
        self.blank_qimage.save(wksavepath)

        wkqim = QImage(wksavepath)
        self.blank_qimage = wkqim

    @QtCore.Slot(object)
    def request_time(self, framenum):

        frame = self.get_frame(framenum)

        if not frame:
            return

        self.frame_ready.emit(frame,framenum)

    def get_frame(self, target_frame):

        # framenumber convert to Sequence index
        offset_frame = int(target_frame - self.seq.start())
        offset_active = int(self.active_time - self.seq.start())
        if offset_frame != offset_active:
            return

        if not self.seq[offset_frame].exists:
            return self.blank_qimage

        qimage = self.toQImage(self.seq[offset_frame].path)

        return qimage

    def get_frame_count(self):

        return len(self.seq) - 1

    def toQImage(self,filepath):

        ibuf = ImageBuf(filepath)
        try:
            bufok = ibuf.read(subimage=0, miplevel=0, force=True, convert=oiio.UINT8)
        except Exception as ex:
            print(ex)
            return None
        if not bufok:
            return None
        spec = ibuf.spec()

        width = spec.width
        height = spec.height

        # Expect the channel to be RGB from the beginning.
        # It might not work if it is a format like ARGB.
        # qimage = QtGui.QImage(width, height, QtGui.QImage.Format_RGB888)
        roi = oiio.ROI(0, width, 0, height, 0, 1, 0, 3)
        try:
            orgimg = Image.fromarray(ibuf.get_pixels(oiio.UINT8,roi))
            # for ImageQt source format error
            if orgimg.mode in self.mw.shot.NO_SUPPORT_IMAGEQT:
                orgimg = orgimg.convert('RGB')
            if self.mw.thumbnail_bright != self.mw.THUMB_DEFALUT_BRIGHT:
                eim = ImageEnhance.Brightness(orgimg)
                orgimg = eim.enhance(self.mw.thumbnail_bright)

            qimage = ImageQt(orgimg)
            # workaround https://bugreports.qt.io/browse/PYSIDE-884
            # output QImage to a file and reRead qimage
            wksavepath = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
            wksavepath = wksavepath + "/{0}/sequencegrab.jpg".format(self.mw.APPID)
            qimage.save(wksavepath, "jpg")
            wkqim = QImage(wksavepath)
            qimage = wkqim
            os.remove(wksavepath)

        except Exception as ex:
            print(ex)
            return None
        return (qimage)
