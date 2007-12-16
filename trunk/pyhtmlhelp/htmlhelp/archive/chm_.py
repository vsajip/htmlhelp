"""Microsoft Compiled HTML Help (CHM) archives support."""


import sys


if sys.platform == "win32":
	from htmlhelp.archive._chm_w32 import ChmArchive
else:
	from htmlhelp.archive._chm_unx import ChmArchive

