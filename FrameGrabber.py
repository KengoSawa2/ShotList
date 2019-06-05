# -*- coding: utf-8 -*-

# FrameGrabber class reference from Pyav/Example/second_seek_example.py

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtCore import Signal

from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageEnhance

import sys
import av

AV_TIME_BASE = 1000000

class FrameGrabber(QtCore.QObject):

    frame_ready = Signal(object, object)
    update_frame_range = Signal(object, object)

    def __init__(self, parent=None,mw=None):
        super(FrameGrabber, self).__init__(parent)
        self.mw = mw
        self.icontainer = None
        self.stream = None
        self.frame = None
        self.active_time = None
        self.start_time = 0
        self.pts_seen = False
        self.nb_frames = None

        self.rate = None
        self.time_base = None

        self.pts_map = {}
        self.total_dur = 0

    def next_frame(self):

        frame_index = None

        rate = self.rate
        time_base = self.time_base

        self.pts_seen = False

        for packet in self.icontainer.demux(self.stream):

            if packet.pts:
                self.pts_seen = True

            for frame in packet.decode():

                if frame_index is None:

                    if self.pts_seen:
                        pts = frame.pts
                    else:
                        pts = frame.dts

                    if not pts is None:
                        frame_index = self.__pts_to_frame(pts, time_base, rate, self.start_time)

                elif not frame_index is None:
                    frame_index += 1

                if not frame.dts in self.pts_map:
                    secs = None

                    if not pts is None:
                        secs = pts * time_base

                    self.pts_map[frame.dts] = secs

                #if frame.pts == None:
                yield frame_index, frame

    @QtCore.Slot(object)
    def request_time(self, second):

        frame = self.get_frame(second)
        if not frame:
            return

        if self.mw.thumbnail_bright != self.mw.THUMB_DEFALUT_BRIGHT:
            wkimage = frame.to_image()

            eim = ImageEnhance.Brightness(wkimage)
            wkimage = eim.enhance(self.mw.thumbnail_bright)

            img = ImageQt(wkimage)
        else:
            rgba = frame.reformat(frame.width, frame.height, "rgb24", 'itu709')
            # could use the buffer interface here instead, some versions of PyQt don't support it for some reason
            # need to track down which version they added support for it
            self.frame = bytearray(rgba.planes[0])
            bytesPerPixel = 3
            img = QtGui.QImage(self.frame, rgba.width, rgba.height, rgba.width * bytesPerPixel, QtGui.QImage.Format_RGB888)

        self.frame_ready.emit(img, second)

    def get_frame(self, target_sec):

        if target_sec != self.active_time:
            return

        rate = self.rate
        time_base = self.time_base

        target_pts = int(target_sec / time_base) + self.start_time
        seek_pts = target_pts  # type: int

        self.icontainer.seek(seek_pts,stream=self.stream)

        last_frame = None

        for i, (frame_index, frame) in enumerate(self.next_frame()):

            if target_sec != self.active_time:
                return

            pts = frame.dts
            if self.pts_seen:
                pts = frame.pts

            if pts > target_pts:
                break

            last_frame = frame

        if last_frame:

            return last_frame

    def get_frame_old(self, target_frame):

        if target_frame != self.active_frame:
            return

        seek_frame = target_frame

        rate = self.rate
        time_base = self.time_base

        frame = None
        reseek = 250

        original_target_frame_pts = None

        while reseek >= 0:

            # convert seek_frame to pts
            target_sec = seek_frame * 1 / rate
            target_pts = int(target_sec / time_base) + self.start_time

            if original_target_frame_pts is None:
                original_target_frame_pts = target_pts

            self.icontainer.seek(int(target_pts),stream=self.stream)

            frame_index = None

            frame_cache = []

            for i, (frame_index, frame) in enumerate(self.next_frame()):

                # optimization if the time slider has changed, the requested frame no longer valid
                if target_frame != self.active_frame:
                    return

                if frame_index is None:
                    pass

                elif frame_index >= target_frame:
                    break

                frame_cache.append(frame)

            # Check if we over seeked, if we over seekd we need to seek to a earlier time
            # but still looking for the target frame
            if frame_index != target_frame:

                if frame_index is None:
                    over_seek = '?'
                else:
                    over_seek = frame_index - target_frame
                    if frame_index > target_frame:

                        # print(over_seek, frame_cache)
                        if over_seek <= len(frame_cache):
                            print("over seeked by %i, using cache" % over_seek)
                            frame = frame_cache[-over_seek]
                            break


                seek_frame -= 1
                reseek -= 1

            else:
                break

        if reseek < 0:
            raise ValueError("seeking failed %i" % frame_index)

        # frame at this point should be the correct frame

        if frame:

            return frame

        else:
            raise ValueError("seeking failed %i" % target_frame)

    def get_frame_count(self):

        frame_count = None

        if self.stream.frames:
            frame_count = self.stream.frames
        elif self.stream.duration:
            frame_count = self.__pts_to_frame(self.stream.duration, float(self.stream.time_base), self.__get_frame_rate(self.stream), 0)
        elif self.icontainer.duration:
            frame_count = self.__pts_to_frame(self.icontainer.duration, 1 / float(AV_TIME_BASE), self.__get_frame_rate(self.stream), 0)
        else:
            raise ValueError("Unable to determine number for frames")

        seek_frame = frame_count
        retry = 100

        while retry:
            target_sec = seek_frame * 1 / self.rate
            target_pts = int(target_sec / self.time_base) + self.start_time

            # self.stream.seek(int(target_pts))
            self.icontainer.seek(int(target_pts),stream=self.stream)

            frame_index = None

            for frame_index, frame in self.next_frame():
                # print(frame_index, frame)
                continue

            if not frame_index is None:
                break
            else:
                seek_frame -= 1
                retry -= 1

        return frame_index or frame_count

    @QtCore.Slot(object)
    def set_container(self, avcontainer):
        self.icontainer = avcontainer
        videolist = []
        for i, s in enumerate(self.icontainer.streams):
            if s.type == 'video': # and self.stream is None:
                videolist.append(s)
            elif s.type == 'data':
                pass
            elif s.type == 'audio':
                pass
            else:
                pass
        self.stream = videolist[0]
        self.rate = self.__get_frame_rate(self.stream)
        self.time_base = float(self.stream.time_base)

        # check unsupported video codec
        if self.stream.codec_context is None:
            raise self.NoSupportCodecException

        index, first_frame = next(self.next_frame())
        if not self.stream.start_time:
            self.icontainer.seek(0,stream=self.stream)
        else:
            self.icontainer.seek(self.stream.start_time,stream=self.stream)

        # find the pts of the first frame
        index, first_frame = next(self.next_frame())

        if self.pts_seen:
            pts = first_frame.pts
        else:
            pts = first_frame.dts

        self.start_time = pts or first_frame.dts

        self.nb_frames = self.get_frame_count()

        dur = None

        if self.stream.duration:
            dur = self.stream.duration * self.time_base
        else:
            dur = self.icontainer.duration * 1.0 / float(AV_TIME_BASE)

        self.total_dur = dur

        self.update_frame_range.emit(dur, self.rate)

    def __pts_to_frame(self,pts, time_base, frame_rate, start_time):
        return int(pts * time_base * frame_rate) - int(start_time * time_base * frame_rate)

    def __get_frame_rate(self,stream):

        if hasattr(stream.average_rate,"denominator") and hasattr(stream.average_rate, "numerator"):
            if stream.average_rate.denominator and stream.average_rate.numerator:
                return float(stream.average_rate)

        elif hasattr(stream.time_base.denominator,"denominator") and hasattr(stream.time_base.numerator,"numerator"):
            if stream.time_base.denominator and stream.time_base.numerator:
                return 1.0 / float(stream.time_base)
        else:
            return(29.974)

    class NoSupportCodecException(Exception):
        pass