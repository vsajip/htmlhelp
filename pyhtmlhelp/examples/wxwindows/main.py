#!/usr/bin/python

import os.path
import sys

from wxPython.wx import *
from wxPython.html import *

from HTMLHelp.generic import read


class file_wrapper:
	"""Hack around a bug in wxPython"""

	def __init__(self, f):
		self.f = f
	
	def __getattr__(self, n):
		return getattr(self.f, n)
	
	def tell(self):
		return long(self.f.tell())
	

class BookFileSystemHandler(wxFileSystemHandler):

	def CanOpen(self, location):
		return self.GetProtocol(location) == 'book'

	def OpenFile(self, fs, location):
		if 0:
			name = self.GetLeftLocation(location)
			link = self.GetRightLocation(location)
		else:
			link = self.GetRightLocation(location)
			words = filter(None, link.split('/'))
			name = words[0]
			link = '/'.join(words[1:])
		book = catalog[name]
		anchor = self.GetAnchor(location)
		mimetype = self.GetMimeTypeFromExt(location)
		stream = wxInputStream(file_wrapper(book.archive[link]))
		return wxFSFile(stream, location, mimetype, anchor, wxDateTime_Now())


wxFileSystem_AddHandler(BookFileSystemHandler())


style_TOOLBAR		= 0x0001
style_CONTENTS		= 0x0002
style_INDEX		= 0x0004
style_SEARCH		= 0x0008
style_BOOKMARKS		= 0x0010
style_OPEN_FILES	= 0x0020
style_PRINT		= 0x0040
style_FLAT_TOOLBAR	= 0x0080
style_MERGE_BOOKS	= 0x0100
style_ICONS_BOOK	= 0x0200
style_ICONS_BOOK_CHAPTER= 0x0400
style_ICONS_FOLDER	= 0x0000 # this is 0 since it is default
style_DEFAULT_STYLE	= (style_TOOLBAR | style_CONTENTS | style_INDEX | style_SEARCH | style_BOOKMARKS | style_PRINT)

id_PANEL		= 1002
id_BACK			= 1003
id_FORWARD		= 1004
id_UPNODE		= 1005
id_UP			= 1006
id_DOWN			= 1007
id_PRINT		= 1008
id_OPENFILE		= 1009
id_OPTIONS		= 1010
id_BOOKMARKSLIST	= 1011
id_BOOKMARKSADD		= 1012
id_BOOKMARKSREMOVE	= 1013
id_TREECTRL		= 1014
id_INDEXPAGE		= 1015
id_INDEXLIST		= 1016
id_INDEXTEXT		= 1017
id_INDEXBUTTON		= 1018
id_INDEXBUTTONALL	= 1019
id_NOTEBOOK		= 1020
id_SEARCHPAGE		= 1021
id_SEARCHTEXT		= 1022
id_SEARCHLIST		= 1023
id_SEARCHBUTTON		= 1024
id_SEARCHCHOICE		= 1025
id_COUNTINFO		= 1026


class MyHtmlWindow(wxHtmlWindow):

	def __init__(self, frame, parent):
		wxHtmlWindow.__init__(self, parent)
		self.frame = frame
		
	def OnLinkClicked(self, link):
		self.frame.NotifyPageChanged()


class BookFrame(wxFrame):

	def __init__(self, parent, id, title, style = style_DEFAULT_STYLE):
		wxFrame.__init__(self, parent, -4, title, style = wxDEFAULT_FRAME_STYLE | wxNO_FULL_REPAINT_ON_RESIZE)

		self.SetIcon(wxArtProvider_GetIcon(wxART_HELP, wxART_HELP_BROWSER))

		# Create the status bar
		self.CreateStatusBar()

		# Create the tool bar
		if style & style_TOOLBAR:
			self.toolBar = self.CreateToolBar(wxNO_BORDER | wxTB_HORIZONTAL | wxTB_FLAT)

			self.toolBar.AddSimpleTool(
				id_PANEL, 
				wxArtProvider_GetBitmap(wxART_HELP_SIDE_PANEL, wxART_HELP_BROWSER), 
				"Show/hide navigation panel")
			self.toolBar.AddSeparator()
			self.toolBar.AddSimpleTool(
				id_BACK, 
				wxArtProvider_GetBitmap(wxART_GO_BACK, wxART_HELP_BROWSER), 
				"Go back")
			self.toolBar.AddSimpleTool(
				id_FORWARD, 
				wxArtProvider_GetBitmap(wxART_GO_FORWARD, wxART_HELP_BROWSER), 
				"Go forward")
			self.toolBar.AddSeparator()
			self.toolBar.AddSimpleTool(
				id_UPNODE, 
				wxArtProvider_GetBitmap(wxART_GO_TO_PARENT, wxART_HELP_BROWSER), 
				"Go one level up in document hierarchy")
			self.toolBar.AddSimpleTool(
				id_UP, 
				wxArtProvider_GetBitmap(wxART_GO_UP, wxART_HELP_BROWSER), 
				"Previous page")
			self.toolBar.AddSimpleTool(
				id_DOWN, 
				wxArtProvider_GetBitmap(wxART_GO_DOWN, wxART_HELP_BROWSER), 
				"Next page")

			if style & style_OPEN_FILES:
				self.toolBar.AddTool(
					id_OPENFILE, 
					wxArtProvider_GetBitmap(wxART_FILE_OPEN, wxART_HELP_BROWSER), 
					"Open HTML document")
		
			if style & style_PRINT:
				self.toolBar.AddSimpleTool(
					id_PRINT, 
					wxArtProvider_GetBitmap(wxART_PRINT, wxART_HELP_BROWSER), 
					"Print this page")

			self.toolBar.Realize()

			EVT_TOOL_RANGE(self, id_PANEL, id_OPTIONS, self.OnToolbar)

		if style & (style_CONTENTS | style_INDEX | style_SEARCH):
			# traditional help controller; splitter window with html page on the
			# right and a notebook containing various pages on the left
			self.splitter = wxSplitterWindow(self, -1)

			self.htmlWindow = MyHtmlWindow(self, self.splitter)
			self.navigationPanel = wxPanel(self.splitter, -1)
			self.navigationNotebook = wxNotebook(self.navigationPanel, id_NOTEBOOK, wxDefaultPosition, wxDefaultSize)
			navigationNotebookSizer = wxNotebookSizer(self.navigationNotebook)
			
			navigationSizer = wxBoxSizer(wxVERTICAL)
			navigationSizer.Add(navigationNotebookSizer, 1, wxEXPAND)

			self.navigationPanel.SetAutoLayout(TRUE)
			self.navigationPanel.SetSizer(navigationSizer)
		else:
			# only html window, no notebook with index,contents etc
			self.htmlWindow = wxHtmlWindow(self)

		self.titleFormat = '%s'
		self.htmlWindow.SetRelatedFrame(self, self.titleFormat)
		self.htmlWindow.SetRelatedStatusBar(0)

		# Create the contents tree panel
		if style & style_CONTENTS:
			contentsPage = wxPanel(self.navigationNotebook, id_INDEXPAGE)
			contentsSizer = wxBoxSizer(wxVERTICAL)
			
			contentsPage.SetAutoLayout(TRUE)
			contentsPage.SetSizer(contentsSizer)

			self.contentsTree = wxTreeCtrl(
				contentsPage, 
				id_TREECTRL, 
				wxDefaultPosition, wxDefaultSize, 
				wxSUNKEN_BORDER | wxTR_HAS_BUTTONS | wxTR_HIDE_ROOT | wxTR_LINES_AT_ROOT)
			
			#contentsTree.AssignImageList(ContentsImageList)
			EVT_TREE_SEL_CHANGED(self, id_TREECTRL, self.OnContentsSel)
			
			contentsSizer.Add(self.contentsTree, 1, wxEXPAND | wxALL)

			self.navigationNotebook.AddPage(contentsPage, "Contents")

		# Create the index list panel
		if style & style_INDEX:
			indexPage = wxPanel(self.navigationNotebook, id_INDEXPAGE);	   
			indexSizer = wxBoxSizer(wxVERTICAL)

			indexPage.SetAutoLayout(TRUE)
			indexPage.SetSizer(indexSizer)

			self.indexText = wxTextCtrl(
				indexPage, 
				id_INDEXTEXT, 
				'', 
				wxDefaultPosition, wxDefaultSize, 
				wxTE_PROCESS_ENTER)
			self.indexList = wxListBox(
				indexPage, 
				id_INDEXLIST, 
				wxDefaultPosition, wxDefaultSize, 
				style = wxLB_SINGLE)

			indexSizer.Add(self.indexText, 0, wxEXPAND | wxALL)
			indexSizer.Add(self.indexList, 1, wxEXPAND | wxALL)

			self.navigationNotebook.AddPage(indexPage, "Index")

		# Create the search list panel
		if style & style_SEARCH:
			searchPage = wxPanel(self.navigationNotebook, id_INDEXPAGE);	   
			searchSizer = wxBoxSizer(wxVERTICAL)

			searchPage.SetAutoLayout(TRUE)
			searchPage.SetSizer(searchSizer)

			self.searchText = wxTextCtrl(searchPage, id_SEARCHTEXT, '', wxDefaultPosition, wxDefaultSize, wxTE_PROCESS_ENTER)
			self.searchChoice = wxChoice(searchPage, id_SEARCHCHOICE, wxDefaultPosition, wxDefaultSize)
			self.searchCaseSensitive = wxCheckBox(searchPage, -1, "Case sensitive")
			self.searchWholeWords = wxCheckBox(searchPage, -1, "Whole words only")
			self.searchList = wxListBox(searchPage, id_SEARCHLIST, wxDefaultPosition, wxDefaultSize, style=wxLB_SINGLE)
										 
			searchSizer.Add(self.searchText, 0, wxEXPAND | wxALL)
			searchSizer.Add(self.searchChoice, 0, wxEXPAND | wxLEFT | wxRIGHT | wxBOTTOM)
			searchSizer.Add(self.searchCaseSensitive, 0, wxLEFT | wxRIGHT)
			searchSizer.Add(self.searchWholeWords, 0, wxLEFT | wxRIGHT)
			searchSizer.Add(self.searchList, 1, wxEXPAND | wxALL)

			self.navigationNotebook.AddPage(searchPage, "Search")

		# Create the bookmark list panel
		if style & style_BOOKMARKS:
			bookmarksPage = wxPanel(self.navigationNotebook, id_INDEXPAGE);	   
			bookmarksSizer = wxBoxSizer(wxVERTICAL)

			bookmarksPage.SetAutoLayout(TRUE)
			bookmarksPage.SetSizer(bookmarksSizer)

			self.bookmarksList = wxListBox(bookmarksPage, id_INDEXLIST, wxDefaultPosition, wxDefaultSize, style=wxLB_SINGLE)

			bookmarksSizer.Add(self.bookmarksList, 1, wxEXPAND | wxALL)

			self.navigationNotebook.AddPage(bookmarksPage, "Bookmarks")

		self.htmlWindow.Show(TRUE)

		#self.RefreshLists()

		if navigationSizer:
			navigationSizer.SetSizeHints(self.navigationPanel)
			self.navigationPanel.Layout()

		self.navigation = 1
		self.sashpos = 250

		# showtime
		if self.navigationPanel and self.splitter:
			self.splitter.SetMinimumPaneSize(20)
			if self.navigation:
				self.splitter.SplitVertically(self.navigationPanel, self.htmlWindow, self.sashpos)

			if self.navigation:
				self.navigationPanel.Show(TRUE)
				self.splitter.SplitVertically(self.navigationPanel, self.htmlWindow, self.sashpos)
			else:
				self.navigationPanel.Show(FALSE)
				self.splitter.Initialize(htmlWindow)

		self.AddBooks()
	
	def AddBooks(self):
		root = self.contentsTree.AddRoot("Books")
		for name, book in catalog.iteritems():
			book.name = name
			self.AddBook(root, book)
		
	def AddBook(self, node, book):
		child = self.contentsTree.AppendItem(node, book.title)
		self.contentsTree.SetPyData(child, (book, book.default_link))
		self.AddContents(child, book, book.contents)
		#self.AddIndex(book, book.index)

	def AddContents(self, tree_node, book, toc_node):
		for toc_child in toc_node:
			if wxUSE_UNICODE:
				name = toc_child.name
			else:
				name = toc_child.name.encode('iso-8859-1', 'replace')
			tree_child = self.contentsTree.AppendItem(tree_node, name)
			self.contentsTree.SetPyData(tree_child, (book, toc_child.link))
			self.AddContents(tree_child, book, toc_child)
		
	def AddIndex(self, book, index):
		for entry in index:
			if wxUSE_UNICODE:
				term = entry.term
			else:
				term = entry.term.encode('iso-8859-1', 'replace')
			self.indexList.Append(term)
		
	def Location(self, book, link):
		return 'book:/%s/%s' % (book.name, link)
	
	def OnContentsSel(self, event):
		item = event.GetItem()
		(book, link) = self.contentsTree.GetPyData(item)
		if 0:
			html = book.get(link).read()
			self.htmlWindow.SetPage(html)
		else:
			location = self.Location(book, link)
			self.htmlWindow.LoadPage(location)
		
	def OnToolbar(self, event):
		if event.GetId() == id_PANEL:
			if not (self.splitter and self.navigationPanel):
				return
		
			if self.splitter.IsSplit():
				self.sashpos = self.splitter.GetSashPosition()
				self.splitter.Unsplit(self.navigationPanel);
				self.navigation = 1
			else:
				self.navigationPanel.Show(TRUE)
				self.htmlWindow.Show(TRUE)
				self.splitter.SplitVertically(self.navigationPanel, self.htmlWindow, self.sashpos)
				self.navigation = 1
		
	def NotifyPageChanged(self):
		pass


def main():
	global catalog
	
	catalog = {}

	for arg in sys.argv[1:]:
		root, ext = os.path.splitext(arg)
		name = os.path.basename(root)
		book = read(arg)
		catalog[name] = book
				
	app = wxPySimpleApp()
	frame = BookFrame(None, -1, "HTML Help Books")
	frame.Show(TRUE)
	app.MainLoop()


if __name__ == "__main__":
	main()
