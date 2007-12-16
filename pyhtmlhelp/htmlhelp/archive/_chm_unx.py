"""Microsoft Compiled HTML Help (CHM) archives support using CHMLIB and
ctypes.
"""

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

import ctypes

import htmlhelp.archive._chmlib as chmlib

from htmlhelp.archive import Archive



def _enumerate(chm, ui, result):
	ui = ui.contents

	assert ui.path.find('\0') == -1

	if ui.path.startswith('/'):
		result.append(ui.path[1:])
	
	return chmlib.CHM_ENUMERATOR_CONTINUE


class ChmArchive(Archive):
	"""Compiled HTML Help (CHM) archive."""

	def __init__(self, path):
		Archive.__init__(self)

		self.chm = chmlib.chm_open(path)

	def __del__(self):
		chmlib.chm_close(self.chm)
	
	def __contains__(self, path):
		return path in self.keys()

	def __getitem__(self, path):
		ui = chmlib.chmUnitInfo()
		result = chmlib.chm_resolve_object(self.chm, '/' + path, ui)
		if result != chmlib.CHM_RESOLVE_SUCCESS:
			raise KeyError, "missing file: %s" % path

		buffer = (ctypes.c_ubyte * ui.length)()
		size = chmlib.chm_retrieve_object(self.chm, ui, buffer, 0L, ui.length)
		
		if size != ui.length:
			raise IOError, "incomplete file: %s\n" % ui.path

		fp = StringIO()
		for c in buffer:
			fp.write(chr(c))
		fp.seek(0)
		return fp

	def keys(self):
		result = []
		chmlib.chm_enumerate(self.chm, chmlib.CHM_ENUMERATE_NORMAL | chmlib.CHM_ENUMERATE_FILES, chmlib.CHM_ENUMERATOR(_enumerate), result)
		return result
	

