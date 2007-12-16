"""Microsoft Compiled HTML Help (CHM) archives support using
comtypes.
"""

import os.path

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

from ctypes import *
from comtypes import *
from comtypes.client import *

from htmlhelp.archive._itss import *

from htmlhelp.archive import Archive


class ChmArchive(Archive):
	"""Compiled HTML Help (CHM) archive."""

	def __init__(self, path):
		Archive.__init__(self)
		
		self.pITStorage = CreateObject(CLSID_ITStorage, CLSCTX_INPROC_SERVER, interface=IITStorage)
		
		wpath = c_wchar_p(path)
		self.pIStorage = self.pITStorage.StgOpenStorage(wpath, None, STGM_READ | STGM_SHARE_DENY_WRITE, None, 0)

	def __del__(self):
		pass
	
	def __contains__(self, path):
		return path in self.keys()

	def __getitem__(self, path):
		pIStorage = self.pIStorage
		
		tail = path
		idx = tail.find('/')
		while idx >= 0:
			#print "####", tail, "######"
			head = tail[:idx]
			tail = tail[idx+1:]
			#print "####", head, tail, "######"
			if not head:
				idx = tail.find('/')
				continue
			wpath = c_wchar_p(head)
			try:
				pIStorage = pIStorage.OpenStorage(wpath, None, STGM_READ | STGM_SHARE_EXCLUSIVE, None, 0)
			except COMError, ex:
				hresult, text, details = ex
				if True: #hresult == STG_E_FILENOTFOUND:
					raise KeyError, "missing dir: %s of %s" % (head, path)
				else:
					raise ex
			idx = tail.find('/')

		wpath = c_wchar_p(tail)
		try:
			pIStream = pIStorage.OpenStream(wpath, None, STGM_READ | STGM_SHARE_EXCLUSIVE, 0)
		except COMError, ex:
			hresult, text, details = ex
			if True: #hresult == STG_E_FILENOTFOUND:
				raise KeyError, "missing file: %s" % path
			else:
				raise ex

		fp = StringIO()
		cb = 8192
		buffer = (c_ubyte * cb)()
		while 1:
			cbRead = pIStream.Read(buffer, cb)
			for i in range(cbRead):
				fp.write(chr(buffer[i]))
			if cbRead < cb:
				break
		
		fp.seek(0)
		return fp

	def _enum(self, result, pIStorage, head = ''):
		pEnum = pIStorage.EnumElements(0, None, 0)
		pEnum.Reset()
		while True:
			ss, fetched = pEnum.Next(1)
			if not fetched:
				break
			assert isinstance(ss.pwcsName, unicode)
			path = head + os.path.normpath(ss.pwcsName)
			#print path, ss.type
			if ss.type == STGTY_STREAM:
				result.append(path)
			if ss.type == STGTY_STORAGE:
				self._enum(result, pIStorage.OpenStorage(ss.pwcsName, None, STGM_READ | STGM_SHARE_EXCLUSIVE, None, 0), path + '/')

			# ss.pwcsName is unicode
			#CoTaskMemFree(ss.pwcsName)
			#ss.pwcsName = None

	def keys(self):
		result = []
		self._enum(result, self.pIStorage)
		return result

