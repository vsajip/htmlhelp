var noSelect = 0;

function onTocSelect(event, book)
{
	var tree = event.target;
	var column = "name";

	/* See http://developer.mozilla.org/en/docs/Tree_Widget_Changes */
	try { column = tree.columns[column]; } catch(er) {}
	
	var link = tree.view.getCellValue(tree.currentIndex, column);

	if(!noSelect && link)
		parent.content.location.href = "page.php/" + book + "/" + link;
}

function parentTreeItem(element)
{
	do
		element = element.parentNode;
	while(element.nodeName != 'treeitem')

	return element;
}

function showTreeItem(tree, item)
{
	if(tree.contentView.getIndexOfItem(item) == -1)
	{
		var parentItem = parentTreeItem(item);
		showTreeItem(tree, parentItem);
		parentItem.setAttribute('open', 'true');
	}
}

function selectTreeItem(tree, item)
{
	noSelect = 1;
	showTreeItem(tree, item);
	var row = tree.contentView.getIndexOfItem(item);
	tree.view.selection.select(row);
	tree.currentIndex = row;
	noSelect = 0;
	tree.treeBoxObject.ensureRowIsVisible(row);
}

function onButtonCommand(event)
{
	var tree = document.getElementById("tree");

	var href = parent.content.location.href;
	var base = document.location.href.replace(/\/tocfrm\.xul\.php\?book=(.*)$/,'/page.php/$1/');

	if(href.substr(0, base.length) == base)
	{
		var link = href.substr(base.length);
		//var elements = document.getElementsByTagName('treecell');
		var elements = tree.contentView.root.getElementsByTagName('treecell');

		for(var i = 0; i < elements.length; ++i)
		{
			if(elements[i].getAttribute('value') == link)
			{
				var item = parentTreeItem(elements[i]);
				selectTreeItem(tree, item);
			}
		}
	}
}

// FIXME: eventually make the sync automatic
//setTimeout("onTimeout()", 1000);

