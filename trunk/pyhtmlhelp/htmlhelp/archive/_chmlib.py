"""Microsoft Compiled HTML Help (CHM) archives support using CHMLIB and
ctypes.
"""

import sys

from ctypes import *

if sys.platform == 'cygwin':
	_chmlib = cdll.LoadLibrary('cygchm-0')
else:
	_chmlib = cdll.LoadLibrary('libchm.so')

CHM_UNCOMPRESSED = 0
CHM_COMPRESSED   = 1

CHM_MAX_PATHLEN  = 512

class chmUnitInfo(Structure):
	_fields_ = [
		("start", c_uint64),
		("length", c_uint64),
		("space", c_int),
		("flags", c_int),
		("path", c_char * (CHM_MAX_PATHLEN + 1))
	]

chm_open = _chmlib.chm_open
chm_open.argtypes = [c_char_p]
chm_open.restype = c_void_p
chm_close = _chmlib.chm_close
chm_close.argtypes = [c_void_p]
chm_close.restype = None

CHM_PARAM_MAX_BLOCKS_CACHED = 0

chm_set_param = _chmlib.chm_set_param
chm_set_param.argtypes = [c_void_p, c_int, c_int]
chm_set_param.restype = None

CHM_RESOLVE_SUCCESS = 0
CHM_RESOLVE_FAILURE = 1

chm_resolve_object = _chmlib.chm_resolve_object
chm_resolve_object.argtypes = [c_void_p, c_char_p, POINTER(chmUnitInfo)]
chm_resolve_object.restype = c_int
chm_retrieve_object = _chmlib.chm_retrieve_object
chm_retrieve_object.argtypes = [c_void_p, POINTER(chmUnitInfo), POINTER(c_ubyte), c_uint64, c_int64]
chm_retrieve_object.restype = c_int64

CHM_ENUMERATE_NORMAL    = 1
CHM_ENUMERATE_META      = 2
CHM_ENUMERATE_SPECIAL   = 4
CHM_ENUMERATE_FILES     = 8
CHM_ENUMERATE_DIRS      = 16
CHM_ENUMERATE_ALL       = 31
CHM_ENUMERATOR_FAILURE  = 0
CHM_ENUMERATOR_CONTINUE = 1
CHM_ENUMERATOR_SUCCESS  = 2

CHM_ENUMERATOR = CFUNCTYPE(c_int, c_void_p, POINTER(chmUnitInfo), py_object)

chm_enumerate = _chmlib.chm_enumerate
chm_enumerate.argtypes = [c_void_p, c_int, CHM_ENUMERATOR, py_object]
chm_enumerate.restype = c_int

chm_enumerate_dir = _chmlib.chm_enumerate_dir
chm_enumerate_dir.argtypes = [c_void_p, c_char_p, c_int, CHM_ENUMERATOR, py_object]
chm_enumerate_dir.restype = c_int

