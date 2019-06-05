# -*- coding: utf-8 -*-

import os
import platform
import sys
import io
import av
import math
import timecode
import OpenImageIO as oiio

from winmacsort import winmacsort

import inspect
import binascii
import pydpx_meta
import pathlib
import xxhash
import xattr
import hashlib

from PySide2.QtCore import QObject
from PySide2.QtCore import QByteArray
from PySide2.QtCore import QBuffer
from PySide2.QtCore import QIODevice
from PySide2.QtCore import QStandardPaths
from PySide2.QtGui import QImage
from PySide2 import QtCore
from PySide2 import QtGui
import xlsxwriter as xlsx
from datetime import datetime

import pprint as pp
from OpenImageIO import ImageBuf

from dateutil.parser import parse
from dateutil.tz import tzlocal
import pyseq

from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageEnhance
from natsort.natsort import natsorted
import RapidCopyEA


sysisDarwin = platform.system() == 'Darwin'
sysisWindows = platform.system() == 'Windows'

class ShotList(QtCore.QThread,QObject):

    __version__ = "1.1.3"

    sig_appendtext = QtCore.Signal(str,bool)
    sig_appendtext_unit = QtCore.Signal(str,object)
    sig_updstatus  = QtCore.Signal(str)
    sig_progress = QtCore.Signal(int)
    sig_showdialog = QtCore.Signal(dict)

    sig_begintimer = QtCore.Signal()
    sig_stoptimer  = QtCore.Signal()

    DEBUGMODE = "DEBUG"

    INPUT_PATH = "INPUTPATH"
    OUTPUT_PATH = "OUTPATH"

    OUTPUT_ROWS = "OUTROWS"       # Row data input when outputting xlsx Input source dictionary list,
                                  # see the contents of inputresultlis
    OUTPUT_COLUMNS = "OUTCOLUMNS" # The COLUMN name list at xlsx output,The contents are the column names

    RUNMODE = "RUNMODE"   # What do you do when you run a thread? Mode flag
    RUNMODE_IMPORT_IMAGES = "ING"
    RUNMODE_OUT_XLSX     = "OXX"

    SUPPORT_STAIMAGES = [".dpx",".tga",".tiff",".tif",".jpg",".jpeg",".exr",".png",".raw",".ari",".dng",".gif",".psd"]
    SUPPORT_MOVIMAGES = [".mov",".mp4",".mxf",".avi"]  # shotlist supports extension

    NO_SUPPORT_IMAGEQT = ["LA","RGBX","RGBa","CMYK","YCbCr","LAB","HSV","I","F"]

    OPT_DEBUG = "DEBUG"
    OPT_XLSXOUTTYPE = "XLSX_OTYPE"
    OPT_XLSXMAXROWS = "XLSX_ROWS"

    EXCEL_MAX_HEIGHT = (546 - 46) # Excel 1 cell max height pixel limit(limit by excel spec)
                                  # -46 is Private adjustment:)
    EXCEL_MAX_WIDTH  = EXCEL_MAX_HEIGHT

    THUMB_DEFAULT_X_POINT = 0.2  # Number of font points when xlsx's column width is decided by pixel
                                 # Appropriate for Office for Mac 2011 if it comes out with pixel / 6.
                                 # Fine adjustment

    DEF_EXCEL_WSMAXLEN = 28 # EXCEL sheet name max = 31
    SHEETNUM_MAX = 10000    # Sheet number max(ShotList determined)
    SHEETROW_MAX = 100      # Sheet per rows max
                            # Current max shot size = 1000000

    def __init__(self, parent=None,jp=None,framegrab=None):

        super(ShotList, self).__init__(parent)
        self.mw = parent
        self.fg = framegrab

        self.starttime = "" # Thread run() start time   (type:datetime)
        self.endtime   = "" # Thread run() finished time(type:datetime)


        self.currentseqno = 0      # current processing seq index
        self.totalseqno = 0        # total seq no(for presearch)
        self.optdict = {}          # option param dict key=option name,value=various types

        self.inputresultlist = []  # Result list created by import process
                                   # The contents are in the dictionary,
                                   # the order in which it was found by searching in the folder.

        self.dochome = ""          # Operation Log storage folder path
        self.debugfd = None        # File descriptor for Debug mode

        self.message = ''     # String buffer for notifying mainwindow of the state in shotlist
        self.errmessages = [] # Error string for notifying mainwindow of the state in shotlist
        self.isjp = jp        # True = jp whether started under Japanese environment, False except Japan
        self.debugdir = "Debug"
        self.req_cancel = False
        self.req_suspend = False
        self.errdict = {}     # Error message dict key = filepath value = message with error content
        self.max_thumb_x = 0
        self.max_thumb_y = 0
        self.xlsx_wrap_columns = [self.mw.AUDIOCH,self.mw.AUDIOSRATE,
                                  self.mw.AUDIOCODEC,self.mw.AUDIOBRATE,self.mw.EXINFO]
        self.xxhash = xxhash.xxh64()
        av.logging.set_level(av.logging.FATAL)

        sys.setrecursionlimit(10000) # from av import logging.
                                     # does not work unless it is set. why? What?

    def reset(self):

        self.currentseqno = 0
        self.totalseqno = 0
        self.inputresultlist = []
        self.optdict = {}
        self.max_thumb_x = 0
        self.max_thumb_y = 0
        self.shotresult = ""
        self.errdict.clear()
        self.errmessages.clear()
        self.req_cancel = False
        self.req_suspend = False

    def setOpt(self,key,value):
        self.optdict[key] = value
        return True

    def setdochome(self,dochome):
        self.dochome = dochome

    def reqsuspend(self,req):
        self.req_suspend = req

    def reqcancel(self,req):
        self.req_cancel = req

    def run(self):

        for key,value in self.optdict.items():
            if key == self.OUTPUT_ROWS:
                pass
            elif key == self.OUTPUT_COLUMNS:
                pass
            else:
                pass
                # print("{0}:{1}".format(key,value))

        self.starttime = datetime.now()
        self.endtime = datetime.now()

        if self.OPT_DEBUG in self.optdict:
            filepath = os.path.join(self.dochome, self.debugdir)
            # DebugDirなければ作成
            if not os.path.exists(filepath):
                os.mkdir(filepath)

            filepath = os.path.join(filepath, self.starttime.strftime("%Y%m%d_%H%M%S") + ".txt")

            try:
                self.debugfd = open(filepath, 'wt', encoding="utf-8")
                self.__write_header(self.debugfd)

            except OSError as oserr:
                self.errdict[oserr.filename] = str(oserr)
                self.errmessages.append(str(oserr))
                self.endtime = datetime.now()

        self.sig_begintimer.emit()

        # Capture shot information in Table Widget
        if self.optdict[self.RUNMODE] == self.RUNMODE_IMPORT_IMAGES:

            self.max_thumb_x = min(self.mw.thumbnail_x,self.EXCEL_MAX_WIDTH)
            self.max_thumb_y = min(self.mw.thumbnail_y,self.EXCEL_MAX_HEIGHT)

            self.__make_imageresult()

        # Xlsx output from TableWidget
        else:
            self.message = "output xlsx"
            self.errmessages.clear()

            try:
                self.__output_xlsx()
            except:
                exc_tuple = sys.exc_info()
                exc_message = str(exc_tuple[0]) + str(exc_tuple[1]) + str(exc_tuple[2])
                self.__debugwrite(exc_message)
                self.errmessages.append(exc_message)
                self.errdict[self.optdict[self.INPUT_PATH]] = exc_message

        if self.OPT_DEBUG in self.optdict:
            try:
                self.debugfd.close()
            except OSError as oserr:
                # self.__debugwrite("self.debugfd close failed err={0}".format(str(oserr)))
                # self.sig_appendtext("self.debugfd open failed err={0}".format(str(oserr)), False)
                self.errdict[oserr.filename] = str(oserr)
                self.errmessages.append(str(oserr))

    def __write_header(self,ofd):

        headerstr =  "Gen from ShotList v({0})\n".format(self.__version__)
        headerstr += "PyAV ver({0})\n".format(av.__version__)
        headerstr += "OIIO ver({0})\n".format(oiio.openimageio_version)

        self.__write(ofd,headerstr)

        headerstr = ""
        headerstr += self.tr("INPUTPATH:{0} mode={1}\n".format(self.optdict[self.INPUT_PATH],self.optdict[self.RUNMODE]))
        if sysisDarwin:
            headerstr += self.tr("OSVer:{0}").format("macOS " + platform.mac_ver()[0]) + "\n"
        else:
            headerstr += self.tr("OSVer:{0}").format(platform.system() + platform.win32_ver()[0]) + "\n"

        self.__write(ofd,headerstr)

    def __write(self,ofd,output):

        try:
            ofd.write(output)
        except (IOError,OSError) as err:
            errormessage = self.tr("write error. reason = {0}").format(str(err))
            self.errmessages.append(errormessage)
            self.errdict[err.filename] = errormessage
            self.__debugwrite(errormessage + "\nloststr\n{0}".format(output))

    def __output_xlsx(self):

        rowslist = self.optdict[self.OUTPUT_ROWS]
        outtype = self.optdict[self.OPT_XLSXOUTTYPE]

        self.currentseqno = 0
        self.totalseqno = len(rowslist)

        if outtype == 0:
            # call multi xlsx files output
            self.__output_multixlsx(rowslist)
        elif outtype == 1:
            self.__output_multiwsxlsx(rowslist)
        else:
            self.__output_onexlsx(rowslist)

    def __output_multixlsx(self,rowslist):

        outpaths = self.optdict[self.OUTPUT_PATH]
        max_row = self.optdict[self.OPT_XLSXMAXROWS]

        iroot = self.optdict[self.INPUT_PATH]
        totalreclen = len(rowslist)
        offset = 0
        outpathindex = 0
        try:
            for i,rec in enumerate(rowslist):
                self.currentseqno += 1
                if i == 0:
                    if totalreclen < max_row:
                        eindex = str(totalreclen)
                    else:
                        eindex = str(max_row)
                    wbtuple = self.__open_wb(outpaths[outpathindex])
                    ws = self.__create_ws(wbtuple[0],wbtuple[1],iroot,"{0}_{1}".format(str(i+1),eindex))

                elif i != 0 and i % max_row == 0:
                    offset = offset - max_row
                    # close current book
                    self.__close_wb(wbtuple[0])
                    outpathindex = outpathindex + 1
                    # next filename
                    if totalreclen - i < max_row:
                        # last file
                        eindex = str(totalreclen)
                    else:
                        eindex = str((i + max_row))

                    # open workbook
                    wbtuple = self.__open_wb(outpaths[outpathindex])

                    # create ws
                    ws = self.__create_ws(wbtuple[0],wbtuple[1],iroot,"{0}_{1}".format(str(i+1),str(eindex)))

                else:
                    # print("i = {0}".format(i))
                    pass

                if self.checkcancel():
                    return
                self.message = self.tr("xlsx output {0}/{1}".format(i, totalreclen))
                self.__output_onerec(i + offset,rec,ws,wbtuple[1])

            self.__close_wb(wbtuple[0])

        except Exception as ex:
            exstr = 'xlsx.Workbook exception:' + str(ex)
            self.errmessages.append(exstr)
            self.errdict[self.optdict[self.OUTPUT_PATH]] = exstr
            self.__debugwrite(exstr)

    def __output_multiwsxlsx(self,rowslist):

        outpath = self.optdict[self.OUTPUT_PATH]
        max_row = self.optdict[self.OPT_XLSXMAXROWS]

        totalreclen = len(rowslist)
        offset = 0
        root = self.optdict[self.INPUT_PATH]
        try:
            wbtuple = self.__open_wb(outpath)

            for i,rec in enumerate(rowslist):

                self.currentseqno += 1

                if i == 0:
                    if totalreclen < max_row:
                        eindex = str(totalreclen)
                    else:
                        eindex = str(max_row)
                    ws = self.__create_ws(wbtuple[0],wbtuple[1],root,"{0}_{1}".format(str(i+1),eindex))
                elif i != 0 and i % max_row == 0:
                    offset = offset - max_row
                    # next wsname
                    if totalreclen - i < max_row:
                        # last ws
                        eindex = str(totalreclen)
                    else:
                        eindex = str((i + max_row))
                    ws = self.__create_ws(wbtuple[0],wbtuple[1],root,"{0}_{1}".format(str(i+1),eindex))
                else:
                    pass

                self.__output_onerec(i + offset,rec,ws,wbtuple[1])
            self.__close_wb(wbtuple[0])
        except Exception as ex:
            exstr = 'xlsx.Workbook exception:' + str(ex)
            self.errmessages.append(exstr)
            self.errdict[self.optdict[self.OUTPUT_PATH]] = exstr
            self.__debugwrite(exstr)

    def __output_onexlsx(self,rowslist):

        outpath = self.optdict[self.OUTPUT_PATH]
        max_row = self.optdict[self.OPT_XLSXMAXROWS]
        totalreclen = len(rowslist)
        root = self.optdict[self.INPUT_PATH]

        try:
            wbtuple = self.__open_wb(outpath)
            ws = self.__create_ws(wbtuple[0],wbtuple[1],root,"{0}_{1}".format(str(1),totalreclen))

            for i, rec in enumerate(rowslist):
                self.currentseqno += 1
                self.__output_onerec(i, rec, ws, wbtuple[1])
            self.__close_wb(wbtuple[0])

        except Exception as ex:
            exstr = 'xlsx.Workbook exception:' + str(ex)
            self.errmessages.append(exstr)
            self.errdict[self.optdict[self.OUTPUT_PATH]] = exstr
            self.__debugwrite(exstr)

    def __open_wb(self,filename):

        wb = None
        try:
            wb = xlsx.Workbook(filename)

            propdict = {}

            wrap_format = wb.add_format({'font_size': 13,'bold': True,'text_wrap': True})
            err_format = wb.add_format({'text_wrap': True, 'bg_color': 'red'})
            linebg_format = wb.add_format({'bg_color': '#EEF3FF', 'border': 1})
            line_format = wb.add_format({'border': 1})
            bold = wb.add_format({'bold': True})
            title = wb.add_format({'font_size': 18,'bold': True})
            column = wb.add_format({'font_size': 13,'bold': True})

            propdict['wrap_format'] = wrap_format
            propdict['err_format'] = err_format
            propdict['linebg_format'] = linebg_format
            propdict['line_format'] = line_format
            propdict['bold'] = bold
            propdict['title'] = title
            propdict['column'] = column

        except Exception as ex:
            raise
        return wb,propdict

    def __close_wb(self,wb):

        isclose_ok = False
        try:
            wb.close()
            isclose_ok = True
        except Exception as ex:
            raise
        return isclose_ok

    def __create_ws(self,wb,propdict,header,wsname):

        ws = None
        try:
            ws = wb.add_worksheet(wsname)
            ws.write_string(0, 0, header, propdict['title'])

            if os.path.exists(self.mw.eyecatch):
                image = QImage(self.mw.eyecatch)
                resize_x = image.width()
                resize_y = image.height()
                if image.height() > self.EXCEL_MAX_HEIGHT:
                    resize_y = self.EXCEL_MAX_HEIGHT
                if image.width() > self.EXCEL_MAX_WIDTH:
                    resize_x = self.EXCEL_MAX_WIDTH
                if resize_x != image.width() or resize_y != image.height():
                    image = image.scaled(resize_x,resize_y,QtCore.Qt.KeepAspectRatio)

                wksavepath = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
                wksavepath = wksavepath + "/{0}/{1}.jpg".format(self.mw.APPID,"eye")

                image.save(wksavepath,"jpg",-1)

                ws.insert_image(0, 1, wksavepath)
                # os.remove(wksavepath)
                ws.set_row(0, image.height())
            # Column header names write
            for i,columnname in enumerate(self.optdict[self.OUTPUT_COLUMNS]):

                if columnname in self.xlsx_wrap_columns:
                    ws.write_string(1, i, columnname,propdict['wrap_format'])
                else:
                    ws.write_string(1, i, columnname,propdict['column'])
        except Exception as ex:
            raise
        return ws

    def __output_onerec(self,i,rec,ws,propdict):
        try:
            rowno = i + 2

            for y, rowdata in enumerate(rec):
                if not rowdata:
                    ws.write(rowno, y, "")
                elif isinstance(rowdata,str):
                    ws.write_string(rowno, y, rowdata)
                else:
                    bytes = QByteArray()
                    buffer = QBuffer(bytes)
                    buffer.open(QIODevice.WriteOnly)
                    rowdata.save(buffer,"jpg")
                    imgByteArr = io.BytesIO(bytes.data())
                    thumb_name = str(i) + str(y) + '.jpg'
                    ws.insert_image(rowno,y,thumb_name,options={'image_data': imgByteArr,'x_offset':5, 'y_offset': 5})
                    ws.set_column(y,y,(rowdata.width() * self.THUMB_DEFAULT_X_POINT))

                    # 奇数の時は色分け
                    if rowno % 2 == 1:
                        ws.set_row(rowno, rowdata.height() + 5, propdict['linebg_format'])
                    else:
                        ws.set_row(rowno, rowdata.height() + 5, propdict['line_format'])
                    buffer.close()

        except Exception as ex:
            raise
        return True

    # Generate internal data from given folder.
    def __make_imageresult(self):

        if os.path.isdir(self.optdict.get(self.INPUT_PATH)):

            try:
                self.__imagefrom_folder(self.optdict[self.INPUT_PATH])
            except:
                exc_tuple = sys.exc_info()
                exc_message = str(exc_tuple[0]) + str(exc_tuple[1]) + str(exc_tuple[2])
                self.__debugwrite(exc_message)
                self.errmessages.append(exc_message)
                self.errdict[self.optdict[self.INPUT_PATH]] = exc_message

        else:
            # Todo: Read the contents of fcpxml and make a shotlist....
            pass

    # Search for an image file that looks like it from the specified folder and make a shot list!
    def __imagefrom_folder(self,folderpath):

        # presearch sequence
        for root, dirs, seqs, files in pyseq.walk(folderpath,onerror=self.__prescan_onerror):

            for seq in seqs:

                # print("pre:" + str(seq))
                if self.checkcancel():
                    return

                ext = os.path.splitext(seq.path())[1].lower()
                if ext in self.SUPPORT_STAIMAGES:

                    strippath = seq.path().lstrip(self.optdict[self.INPUT_PATH])

                    self.__debugwrite("presearch root. {1}/{1} {0} shots".format(seq.path(),self.totalseqno))
                    self.message = self.tr("presearch {1}/{1} {0} shots".format(strippath,self.totalseqno))
                    self.totalseqno += 1
                    # print("pre seq = {0} ext = {1}".format(seq.path(),ext))

                elif ext in self.SUPPORT_MOVIMAGES:
                    pass
                else:
                    pass

            for file in natsorted(files):
                ext = os.path.splitext(file)[1].lower()
                # Still images already processed with seq
                if ext in self.SUPPORT_STAIMAGES:
                    pass
                elif ext in self.SUPPORT_MOVIMAGES:
                    fullpath = os.path.join(root,file)
                    strippath = fullpath.lstrip(self.optdict[self.INPUT_PATH])
                    self.__debugwrite("presearch root. {1}/{1} {0} shots".format(fullpath, self.totalseqno))
                    self.message = self.tr("presearch {1}/{1} {0} shots".format(strippath, self.totalseqno))
                    self.totalseqno += 1
                else:
                    pass
            # Adjust to folder display order specific to Mac/Win
            winmacsort(dirs)

        # Recursively loop through folders in sequence units
        for root, dirs, seqs, files in pyseq.walk(folderpath):

            self.__debugwrite("process root. {0}".format(root))

            for seq in seqs:

                if self.checkcancel():
                    return

                ext = os.path.splitext(seq.path())[1].lower()

                if ext in self.SUPPORT_STAIMAGES:

                    if self.mw.disableseq:
                        pass
                    else:
                        self.__generate_rowdata(root, seq, False, ext)

                elif ext in self.SUPPORT_MOVIMAGES:
                    pass

                else:
                    pass

            # Priority of filename is '-' or '_' Priority processing is inconvenient
            for file in natsorted(files):
                ext = os.path.splitext(file)[1].lower()

                if self.checkcancel():
                    return
                # For still images already processed with seq section
                if ext in self.SUPPORT_STAIMAGES:
                    if self.mw.disableseq:
                        # It's nonsense ....:(
                        mylist = []
                        mylist.append(file)
                        myseq = pyseq.Sequence(mylist)
                        self.__generate_rowdata(root, myseq, False, ext)
                    else:
                        pass
                elif ext in self.SUPPORT_MOVIMAGES:
                    mylist = []
                    mylist.append(pyseq.Item(file))
                    myseq = pyseq.Sequence(mylist)
                    # myseq.append(myitem)

                    self.__generate_rowdata(root,myseq,True,ext)
                else:
                    pass

            winmacsort(dirs)

    # Extracts one line information and stores it as dict.
    def __generate_rowdata(self,root,seq,ismov,ext):

        rowdata_dict = {}
        rowdata_dict[self.mw.NO] = self.currentseqno + 1 # start index=1
        strippath = seq.path().lstrip(self.optdict[self.INPUT_PATH])
        self.message = self.tr("importing {1}/{2} {0}".format(strippath,self.currentseqno,self.totalseqno))

        self.currentseqno += 1
        rowdata_dict[self.mw.THUMB_S] = "No Image"
        rowdata_dict[self.mw.THUMB_C] = "No Image"
        rowdata_dict[self.mw.THUMB_E] = "No Image"

        rowdata_dict[self.mw.FILENAME] = seq.format('%h%r%t')

        # 0byte garbage file check and unstable file handle check.
        try:
            if seq.size == 0:
                errmessage = self.tr("0 bytes file skipped path = {0}".format(seq.path()))
                self.errmessages.append(errmessage)
                self.errdict[seq.path()] = errmessage
                return
                # print("0byte file skipped")
        except Exception as ex:
            exstr = 'seq.size() exception: file is broken or unstable? ' + os.path.join(root, seq.name) + " " + str(ex)
            self.errmessages.append(exstr)
            self.errdict[os.path.join(root, seq.name)] = exstr
            self.__debugwrite(exstr)
            return

        # TODO:SCENE,CUT slice from Filename pattern
        # ex A001_C006_00000.dpx -> SCENE:A001 CUT:C006
        # pattern spec copied from BMD Resolve import pattern matching spec:)
        rowdata_dict[self.mw.SCENE] = ""
        rowdata_dict[self.mw.CUT] = ""
        rowdata_dict[self.mw.TAKE] = ""
        rowdata_dict[self.mw.COMMENT] = ""
        rowdata_dict[self.mw.CONTAINER] = ext
        rowdata_dict[self.mw.CODEC] = ""
        rowdata_dict[self.mw.PIXSIZE] = ""
        rowdata_dict[self.mw.FILESIZE_GB] = str(round(seq.size / (1024 * 1024 * 1024),2))
        rowdata_dict[self.mw.FILESIZE_MB] = str(round(seq.size / (1024 * 1024), 2))
        rowdata_dict[self.mw.REEL] = ""
        rowdata_dict[self.mw.FPS] = ""
        rowdata_dict[self.mw.SENSORFPS] = ""
        rowdata_dict[self.mw.LENGTH] = ""
        rowdata_dict[self.mw.TC] = ""
        rowdata_dict[self.mw.BIT] = "Unknown"
        rowdata_dict[self.mw.ALPHA] = ""
        rowdata_dict[self.mw.COLORSPACE] = ""
        rowdata_dict[self.mw.GAMMA] = ""
        rowdata_dict[self.mw.AUDIOCH] = ""
        rowdata_dict[self.mw.AUDIOSRATE] = ""
        rowdata_dict[self.mw.AUDIOCODEC] = ""
        rowdata_dict[self.mw.AUDIOBRATE] = ""
        rowdata_dict[self.mw.CREATETIME] = ""

        rowdata_dict[self.mw.FULLPATH] = root
        rowdata_dict[self.mw.RELPATH] = pathlib.Path(root).relative_to(self.optdict[self.INPUT_PATH])
        rowdata_dict[self.mw.CHECKSUM] = ""
        rowdata_dict[self.mw.EXINFO] = ""

        # hidden
        rowdata_dict[self.mw.DIRPATH_HIDDEN] = None
        rowdata_dict[self.mw.FILENAME_HIDDEN] = None
        rowdata_dict[self.mw.SEQPATH_HIDDEN] = None
        rowdata_dict[self.mw.SEQ_HIDDEN_S] = None
        rowdata_dict[self.mw.SEQ_HIDDEN_C] = None
        rowdata_dict[self.mw.SEQ_HIDDEN_E] = None

        file_path = os.path.join(root,seq[0])
        if self.OPT_DEBUG in self.optdict:
            self.errmessages.append(self.tr("importing {0}").format(file_path))

        self.__debugwrite(self.tr("process seq. {0}").format(os.path.join(root,seq.name)))

        if ismov:
            try:
                # container = av.open(os.path.join(root,seq.name), 'r',metadata_errors='replace')
                container = av.open(os.path.join(root,seq.name), 'r',metadata_encoding='utf-8',metadata_errors='ignore')
            except Exception as ex:
                # exstr = 'av.open() exception:' + os.path.join(root, seq.name) + " " + str(ex)
                exstr = self.tr("File open error. detail={0}".format(str(ex)))
                if ext == ".mxf":
                    exstr += self.tr("No support mxf(op-atom):(")
                self.errmessages.append(exstr)
                self.errdict[os.path.join(root,seq.name)] = exstr
                self.__debugwrite(exstr)
                return

            videolist = []
            datalist =  []
            audiolist = []
            containermeta = container.metadata

            # print("Debug containermeta:")
            # for key,value in containermeta.items():
            #     print(" key:{0} value:{1}".format(key,value))

            # pull out video,audio,data stream(s)
            for i,s in enumerate(container.streams):
                # If there are multiple video streams, only handle the first stream.
                if s.type == 'video': # and video is None:
                    videolist.append(s)
                    #print("video stream = #{0}".format(i))
                elif s.type == 'data':
                    datalist.append(s)
                    #print("data stream = #{0}".format(i))
                elif s.type == 'audio':
                    audiolist.append(s)
                    #print("audio stream = #{0}".fo
                    # rmat(i))
                else:
                    exstr = "skip unknown stream: s#{0} type={1}".format(i,type)
                    self.errmessages.append(exstr)
                    self.__debugwrite(exstr)

            # get audio channels data
            # streamslist = []
            audiostreams = 1
            for audio in audiolist:

                rowdata_dict[self.mw.AUDIOCH] += "#{0}:{1}ch".format(audiostreams,audio.channels)
                rowdata_dict[self.mw.AUDIOSRATE] += "#{0}:{1}khz".format(audiostreams,audio.rate / 1000)
                rowdata_dict[self.mw.AUDIOCODEC] += "#{0}:{1}".format(audiostreams,audio.name)
                rowdata_dict[self.mw.AUDIOBRATE] += "#{0}:{1}kb/s".format(audiostreams,int(audio.bit_rate / 1000))
                if audiostreams != len(audiolist):
                    rowdata_dict[self.mw.AUDIOCH] += "\n"
                    rowdata_dict[self.mw.AUDIOSRATE] += "\n"
                    rowdata_dict[self.mw.AUDIOCODEC] += "\n"
                    rowdata_dict[self.mw.AUDIOBRATE] += "\n"
                audiostreams += 1

            # data stream check for reel and TC
            for data in datalist:
                if data.metadata.get('reel_name'):
                    rowdata_dict[self.mw.REEL] = data.metadata['reel_name']
                if data.metadata.get('timecode'):
                    rowdata_dict[self.mw.TC] = data.metadata['timecode']

            # Normally,pick up metadata from the data stream,
            # But,If no metadata in data stream,pick up from video.metadata
            # prores metadata is here.
            if containermeta.get("timecode"):
                rowdata_dict[self.mw.TC] = containermeta['timecode']

            # It seems that both data are contained in UTC.
            if containermeta.get("modification_date"):
                # print(containermeta['modification_date'])
                rowdata_dict[self.mw.CREATETIME] = containermeta['modification_date']

            # metadata dict convert to str
            ex_str = ""
            for k, (key, value) in enumerate(sorted(containermeta.items())):
                ex_str += "{0}:{1}".format(key,value)
                if k + 1 != len(containermeta):
                    ex_str += "\n"
                if key == "com.arri.camera.SensorFps":
                    rowdata_dict[self.mw.SENSORFPS] = str(round(int(value) / 1000,2))

            rowdata_dict[self.mw.EXINFO] = ex_str

            if len(videolist):
                # video,data may have multiple streams,
                # I don't know which stream I should select.
                # For now, I will deal with what I found first stream.
                video = videolist[0]
            else:
                # if file does not have video stream(ex:audio only mxf)
                rowdata_dict[self.mw.THUMB_S] = "Sound Only"
                rowdata_dict[self.mw.THUMB_C] = "Sound Only"
                rowdata_dict[self.mw.THUMB_E] = "Sound Only"
                self.inputresultlist.append(rowdata_dict)
                return

            try:
                self.fg.set_container(container)
            except self.fg.NoSupportCodecException as usex:
                rowdata_dict[self.mw.THUMB_S] = "Unsupported"
                rowdata_dict[self.mw.THUMB_C] = "Unsupported"
                rowdata_dict[self.mw.THUMB_E] = "Unsupported"
                exstr = "ImportError:unsupported format(codec) {0}".format(os.path.join(root,seq.name))
                self.errmessages.append(exstr)
                self.errdict[os.path.join(root,seq.name)] = exstr
                self.__debugwrite(exstr)
                self.inputresultlist.append(rowdata_dict)
                return
            except Exception as ex:
                exstr = "ImportError: detail:{0} {1}".format(str(ex),os.path.join(root,seq.name))
                self.errmessages.append(exstr)
                self.errdict[os.path.join(root,seq.name)] = exstr
                self.__debugwrite(exstr)
                # broken data set???
                self.inputresultlist.append(rowdata_dict)
                return

            frames = 0

            if hasattr(video,"frames") and video.frames != 0:
                # prores has video.frames...
                frames = video.frames
            elif hasattr(video,"duration") and video.duration != 0:
                # mxf has video.duration...
                frames = video.duration
            else:
                pass

            for column in self.mw.columnlist:

                try:
                    if column == self.mw.THUMB_S:
                        self.fg.active_time = self.mw.startoffset
                        # frame = self.fg.get_frame(self.mw.startoffset)
                    elif column == self.mw.THUMB_C:
                        self.fg.active_time = (self.fg.total_dur / 2)
                        self.fg.active_time += self.mw.centeroffset
                    elif column == self.mw.THUMB_E:
                        self.fg.active_time = self.fg.total_dur
                        self.fg.active_time += self.mw.endoffset
                    else:
                        continue
                    # seek range error check and fix
                    if self.fg.active_time > self.fg.total_dur:
                        self.fg.active_time = self.fg.total_dur
                    elif self.fg.active_time < 0.0166666:
                        self.fg.active_time = 0.0

                    frame = None
                    while (frame == None):
                        frame = self.fg.get_frame(self.fg.active_time)
                        self.fg.active_time = self.fg.active_time - 0.0166666

                    wkimage = frame.to_image()

                    if self.mw.thumbnail_bright != self.mw.THUMB_DEFALUT_BRIGHT:
                        eim = ImageEnhance.Brightness(wkimage)
                        wkimage = eim.enhance(self.mw.thumbnail_bright)

                    xy = self.resize_xandy(wkimage.width, wkimage.height)
                    # QPixmap: It is not safe to use pixmaps outside the GUI thread
                    qim = ImageQt(wkimage.resize(xy))

                    # workaround https://bugreports.qt.io/browse/PYSIDE-884
                    # output QImage to a file and reRead qimage
                    wksavepath = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
                    wksavepath = wksavepath + "/{0}/{1}.jpg".format(self.mw.APPID,self.currentseqno)
                    # print(wksavepath)

                    qim.save(wksavepath,"jpg",-1)
                    wkqim = QImage(wksavepath)
                    rowdata_dict[column] = wkqim
                    os.remove(wksavepath)

                    rowdata_dict[self.mw.DIRPATH_HIDDEN] = os.path.dirname(file_path)
                    rowdata_dict[self.mw.FILENAME_HIDDEN] = os.path.basename(file_path)

                except Exception as ex:
                    errstr = "wkimage.to_image() error. path={0} err={1}".format(file_path, str(ex))
                    # print(errstr)
                    self.errmessages.append(errstr)
                    self.errdict[file_path] = errstr
                    self.__debugwrite(errstr)
                    rowdata_dict[column] = "No Image"

            # prores metadata dictionary contains codec information

            if video.metadata.get('encoder'):
                rowdata_dict[self.mw.CODEC] = video.metadata['encoder']
            elif video.metadata.get('long_name'):
                rowdata_dict[self.mw.CODEC] = video.format.long_name
            elif video.metadata.get('name'):
                rowdata_dict[self.mw.CODEC] = video.format.name
            elif hasattr(video,"long_name"):
                rowdata_dict[self.mw.CODEC] = video.long_name
            elif hasattr(video,"name"):
                rowdata_dict[self.mw.CODEC] = video.name
            else:
                rowdata_dict[self.mw.CODEC] = "Unknown"

            rowdata_dict[self.mw.PIXSIZE] = "{0}*{1}".format(str(video.width), str(video.height))

            # for illegal numerator,denominator value exception(zero divide)
            try:
                fps_float = round((video.r_rate.numerator / video.r_rate.denominator), 2)

                if fps_float.is_integer():
                    fps_float = int(fps_float)
            except ZeroDivisionError as zdex:
                fps_float = 0.0

            rowdata_dict[self.mw.FPS] = fps_float

            rowdata_dict[self.mw.LENGTH] = self.__get_TClength(str(rowdata_dict[self.mw.FPS]),frames,seq.name)

            if video.metadata.get('timecode'):
                rowdata_dict[self.mw.TC] = video.metadata['timecode']

            if hasattr(video.format,"name"):
                rowdata_dict[self.mw.BIT] = video.format.name
            if video.metadata.get("creation_time"):
                rowdata_dict[self.mw.CREATETIME] = video.metadata['creation_time']

            if rowdata_dict[self.mw.CREATETIME]:
                # Because it is hard to read time data
                # timezone is UTC so convert it to local
                rowdata_dict[self.mw.CREATETIME] = parse(rowdata_dict[self.mw.CREATETIME]).astimezone(tzlocal())
                rowdata_dict[self.mw.CREATETIME] = rowdata_dict[self.mw.CREATETIME].strftime("%Y/%m/%d %H:%M:%S")

            if self.mw.CHECKSUM in self.mw.columnlist:
                rowdata_dict[self.mw.CHECKSUM] = self.__calc_checksum(seq.path())
        else:
            try:
                self.__setmeta_sta(seq, rowdata_dict, ext)
            except Exception as ex:
                exstr = '__setmeta_sta exception: data broken?' + os.path.join(root, seq.name) + " " + str(ex)
                self.errmessages.append(exstr)
                self.errdict[os.path.join(root, seq.name)] = exstr
                self.__debugwrite(exstr)
                return

            # If fps read from seq,use file fps
            if rowdata_dict[self.mw.FPS]:
                fps = float(rowdata_dict[self.mw.FPS])
            else:
                fps = self.mw.stafps
                # fps = float()

            namelist = []
            for item in seq:
                namelist.append(item.name)

            missingseqs = seq.get_missinglist()

            if missingseqs:
                for missingseq in missingseqs:
                    for item in missingseq:
                        namelist.append(item.name)
                namelist.sort()

            rowdata_dict[self.mw.DIRPATH_HIDDEN] = os.path.dirname(seq[0].path)
            rowdata_dict[self.mw.FILENAME_HIDDEN] = os.path.basename(seq[0].path)
            rowdata_dict[self.mw.SEQPATH_HIDDEN] = namelist

            framenum = len(seq)

            if self.mw.THUMB_S in self.mw.columnlist:
                startframe = self.__stafps_to_framenum(self.mw.startoffset,fps,framenum)
                file_path = seq[startframe].path
                rowdata_dict[self.mw.THUMB_S] = self.toQImage(file_path)
                rowdata_dict[self.mw.SEQ_HIDDEN_S] = file_path

            if self.mw.THUMB_C in self.mw.columnlist:
                if framenum == 1:
                    midframe = 0
                elif (framenum == 2):
                    midframe = 1
                else:
                    midframe = math.ceil(len(seq) / 2) - 1
                # print("midframe:" + str(int(midframe)))
                file_path = seq[midframe].path
                rowdata_dict[self.mw.THUMB_C] = self.toQImage(file_path)
                rowdata_dict[self.mw.SEQ_HIDDEN_C] = file_path

            if self.mw.THUMB_E in self.mw.columnlist:
                # print("lastframe:" + str(framenum - 1))
                file_path = seq[framenum - 1].path
                rowdata_dict[self.mw.THUMB_E] = self.toQImage(file_path)
                rowdata_dict[self.mw.SEQ_HIDDEN_E] = file_path

        self.inputresultlist.append(rowdata_dict)

    def __debugwrite(self,message):
        if self.OPT_DEBUG in self.optdict:
            frame = inspect.currentframe().f_back
            frame_co = frame.f_code

            fixmessage = "debug: func={0} line={1} message = {2}".format(frame_co.co_name,frame.f_lineno,message)
            # print(fixmessage)
            try:
                self.debugfd.write(fixmessage + '\n')
                self.debugfd.flush()
            except IOError as ioerr:
                self.errmessages.append(fixmessage)
                pass

    def resize_xandy(self,x,y):

        while (x > self.max_thumb_x and y > self.max_thumb_y):

            x = (int)(x * 0.9)
            y = (int)(y * 0.9)

        # Forcibly cutting data that is extremely long vertical or horizontal,
        # such as movie telop or event drawing picture.
        if(x > self.EXCEL_MAX_WIDTH):
            x = self.EXCEL_MAX_WIDTH - 100
        if(y > self.EXCEL_MAX_HEIGHT):
            y = self.EXCEL_MAX_HEIGHT - 100

        return(x,y)

    # Passing the total seconds as an int returns "dd:hh:mm:ss" as string
    def __time_f(self,secs):

        pos = abs(int(secs))
        day = pos / (3600*24)
        rem = pos % (3600*24)
        hour = rem / 3600
        abshour = float(pos) / 3600
        rem = rem % 3600
        mins = rem / 60
        secs = rem % 60
        res = '%dd %02d:%02d:%02d (%.1fh)' % (day, hour, mins, secs, abshour)
        if int(secs) < 0:
            res = "-%s" % res
        return res

    def toQImage(self,filepath):

        qimage = "No Image"
        ibuf = ImageBuf(filepath)
        try:
            bufok = ibuf.read(subimage=0, miplevel=0, force=True, convert=oiio.UINT8)
        except Exception as ex:
            self.errmessages.append(str(ex) + " oiioerror:" + oiio.geterror())
            self.__debugwrite(str(ex) + " oiioerror:" + oiio.geterror())
            return qimage
        if not bufok:
            return qimage
        spec = ibuf.spec()
        width = spec.width
        height = spec.height

        # Expect the channel to be RGB from the beginning.
        # It might not work if it is a format like ARGB.
        roi = oiio.ROI(0, width, 0, height, 0, 1, 0, 3)
        try:
            orgimg = Image.fromarray(ibuf.get_pixels(oiio.UINT8,roi))
            # for ImageQt source format error
            if orgimg.mode in self.NO_SUPPORT_IMAGEQT:
                orgimg = orgimg.convert('RGB')
            if self.mw.thumbnail_bright != self.mw.THUMB_DEFALUT_BRIGHT:
                eim = ImageEnhance.Brightness(orgimg)
                orgimg = eim.enhance(self.mw.thumbnail_bright)

            qimage = ImageQt(orgimg.resize(self.resize_xandy(width, height)))
            # workaround https://bugreports.qt.io/browse/PYSIDE-884
            # output QImage to a file and reRead qimage
            wksavepath = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
            wksavepath = wksavepath + "/{0}/{1}.jpg".format(self.mw.APPID, self.currentseqno)
            qimage.save(wksavepath,"jpg",-1)
            wkqim = QImage(wksavepath)
            qimage = wkqim
            os.remove(wksavepath)

        except Exception as ex:
            self.__debugwrite(str(ex))
            ibuf.clear()
            return qimage

        orgimg.close()
        ibuf.clear()

        return (qimage)

    # set Image file meta to dict
    def __setmeta_sta(self,seq,dict,ext):

        spec = ImageBuf(seq[0].path).spec()
        exstr = ""

        bits = spec.getattribute("oiio:BitsPerSample",oiio.TypeInt)
        if bits:
            dict[self.mw.BIT] = str(bits)
        if spec.alpha_channel != -1:
            dict[self.mw.ALPHA] = "Yes"
        else:
            dict[self.mw.ALPHA] = "No"

        dict[self.mw.PIXSIZE] = "{0}*{1}".format(str(spec.width), str(spec.height))

        ctime = spec.getattribute("DateTime", oiio.TypeString)
        if ctime:
            dict[self.mw.CREATETIME] = ctime

        cspace = spec.getattribute("oiio:ColorSpace",oiio.TypeString)
        if cspace:
            dict[self.mw.COLORSPACE] = cspace

        gamma = spec.getattribute("oiio:Gamma",oiio.TypeFloat)
        if gamma:
            dict[self.mw.GAMMA] = str(gamma)

        if ext == '.dpx':
            dpxmeta = pydpx_meta.DpxHeaderEx(seq[0].path)
            dict[self.mw.REEL] = dpxmeta.orient_header.input_name
            dict[self.mw.TC] = dpxmeta.tv_header.time_code
            dict[self.mw.BIT] = str(dpxmeta.image_header.image_element[0].bit_size)

            if not math.isnan(dpxmeta.film_header.frame_rate) and not dpxmeta.film_header.frame_rate == float("inf") \
                    and dpxmeta.film_header.frame_rate and dpxmeta.film_header.frame_rate > 0:
                f_value = round(dpxmeta.film_header.frame_rate, 2)
                if f_value == 0.0:
                    dict[self.mw.FPS] = ""
                else:
                    dict[self.mw.FPS] = str(f_value)
            elif not math.isnan(dpxmeta.tv_header.frame_rate) and dpxmeta.tv_header.frame_rate and dpxmeta.tv_header.frame_rate > 0:
                f_value = round(dpxmeta.tv_header.frame_rate, 2)
                if f_value == 0.0:
                    dict[self.mw.FPS] = ""
                else:
                    dict[self.mw.FPS] = str(f_value)
            else:
                dict[self.mw.FPS] = ""

            dict[self.mw.LENGTH] = self.__get_TClength(dict[self.mw.FPS],seq.length(),seq[0].path)

            if math.isnan(dpxmeta.tv_header.gamma):
                dict[self.mw.GAMMA] = ""
            else:
                dict[self.mw.GAMMA] = str(dpxmeta.tv_header.gamma)

        elif ext == '.tga':
            comp = spec.getattribute("Compression",oiio.TypeString)
            if comp:
                dict[self.mw.CODEC] = comp

            pass
        elif ext == '.tif' or ext == '.tiff':
            comp = spec.getattribute("compression",oiio.TypeString)
            if comp:
                dict[self.mw.CODEC] = comp

        elif ext == '.jpg' or ext == '.jpeg':
            pass
        elif ext == '.exr':

            dict["bitdepth"] = str(spec.format)

            for i in range(len(spec.channelnames)):
                exstr += "ch{0}:".format(i+1)
                exstr += spec.channelnames[i] + "\n"

            fps = spec.getattribute("FramesPerSecond",oiio.TypeRational)
            if fps and fps[0] > 0 and fps[1] > 0:
                dict[self.mw.FPS] = str(round(fps[0] / fps[1],2))
            else:
                dict[self.mw.FPS] = ""
            comp = spec.getattribute("compression",oiio.TypeString)
            if comp:
                dict[self.mw.CODEC] = comp

            time_code_str = ""
            tc = spec.getattribute("smpte:TimeCode",oiio.TypeTimeCode)
            if tc:
                time_code_tmp = '{0:0>8x}'.format(tc[0])
                time_code_str = "{0}:{1}:{2}:{3}".format(time_code_tmp[0:2],time_code_tmp[2:4],
                                                         time_code_tmp[4:6],time_code_tmp[6:8])
            dict[self.mw.TC] = time_code_str
            dict[self.mw.EXINFO] = exstr

        elif ext == '.png':
            pass
        elif ext == '.gif':
            pass

        elif ext == '.raw' or ext == '.ari' or ext == '.dng':
            cspace = spec.getattribute("raw:ColorSpace", oiio.TypeString)
            if cspace:
                dict[self.mw.COLORSPACE] = cspace
        elif ext == '.psd':
            pass
        else:
            pass

        dict[self.mw.LENGTH] = self.__get_TClength(str(dict['fps']), len(seq),seq[0].path)

    # fps
    def __get_TClength(self,fps_str,framelen,filename):

        return_str = "Unknown"

        if fps_str and fps_str != "0.0":
            try:
                # for ARRISCAN dpx fpsstr
                if fps_str == '24.0' or fps_str == '30.0' or fps_str == '60.0':
                    fps_str = int(float(fps_str))
                # print(fps_str)
                delta_tc = timecode.Timecode(fps_str, "00:00:00:00")
                delta_tc += framelen
                return_str = str(delta_tc)
            except Exception as ex:
                # print(str(ex))
                self.__debugwrite(filename + fps_str + str(ex))
                # print(traceback.format_exc())
                # print(filename + fps_str)
                return_str = str(framelen) + "Frame"
        else:
            return_str = str(framelen) + "Frame"

        return return_str

    def __stafps_to_framenum(self,secmsec,fps,framenum):

        s = int(secmsec)
        ms = (secmsec - s) * 1000
        s = s * 1000
        setms = s + ms

        totalsec = framenum / fps
        ts = int(totalsec)
        tms = (totalsec - ts) * 1000
        ts = ts * 1000
        settms = ts + tms

        # Specified frame does not exist?(over)
        if setms >= settms:
            # none frame. last frame set
            targetframe = framenum - 1
        else:
            targetframe = int(setms / (1000 / fps))

        return targetframe

    def __calc_checksum(self,path):

        checksumstr = "*"
        if not os.path.exists(path):
            return checksumstr
        elif os.path.islink(path):
            if os.stat(path).st_size == 0:
                return checksumstr
        elif os.stat(path).st_size == 0:
            return checksumstr

        # check RapidCopy EA
        try:
            attr = xattr.getxattr(path, "com.rapidcopy.checksum")
            ea = RapidCopyEA.EAStructure()
            buffer = io.BytesIO(attr)
            return_size = buffer.readinto(ea)

            #EA size error
            if return_size != 128:
                raise EnvironmentError("EAcheck:EA size invalid")
            # EA saved original filesize difference
            elif ea.f_size != os.stat(path).st_size:
                raise EnvironmentError("EAcheck:File size diffrence")
            # RapidCopy checksum type difference
            elif self.mw.CHECK_ALGO_DICT[ea.ctype] != self.mw.checksumalgo:
                raise EnvironmentError("EAcheck:checksum algo diffrence")
            # RapidCopy write finished time difference
            elif ea.endtime != int(os.stat(path).st_ctime):
                raise EnvironmentError("EAcheck:ctime difference")
            checksumstr = str(binascii.hexlify(ea.checksum), 'utf-8')

        except EnvironmentError as eerr:
            # print(eerr)
            pass

        if checksumstr == "*":
            try:
                with open(path, 'rb') as f:
                    # md5
                    if self.mw.checksumalgo == self.mw.CHECK_ALGO_XXHASH:
                        self.xxhash.reset()
                        calc = self.xxhash
                    # sha1
                    elif self.mw.checksumalgo == self.mw.CHECK_ALGO_MD5:
                        calc = hashlib.md5()
                    # xxhash
                    elif self.mw.checksumalgo == self.mw.CHECK_ALGO_SHA1:
                        calc = hashlib.sha1()

                    while True:
                        if self.checkcancel():
                            checksumstr = "*"
                            return (checksumstr)

                        buf = f.read(4096)
                        if not buf:
                            break
                        calc.update(buf)
                    checksumstr = calc.hexdigest()

            except OSError as oserr:
                # error syori
                checksumstr = "Read Error"
        return (checksumstr)

    def checkcancel(self):

        while self.req_suspend:
            self.sleep(1)

        if self.req_cancel:
            return(True)
        else:
            return(False)

    def __prescan_onerror(self,oserror):
        pass

if __name__ == '__main__':
    import sys
    import ShotList_rc
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from mainwindow import MainWindow

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)

    window.show()
    if sysisDarwin:
        window.raise_()
    sys.exit(app.exec_())