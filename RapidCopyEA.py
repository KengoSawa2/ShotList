# -*- coding: utf-8 -*-

from ctypes import *

class EAStructure(Structure):
    _fields_ = (
        ('size', c_ushort),
        ('ver', c_ushort),
        ('subver', c_ushort),
        ('ctype', c_ushort),
        ('f_size', c_int64),
        ('endtime', c_int64),
        ('c_reserve2', c_char * 8),
        ('start_eye', c_char * 16),
        ('checksum', c_char * 32),
        ('end_eye', c_char * 16),
        ('date_eye', c_char * 16),
        ('size_eye', c_char * 16),
    )

