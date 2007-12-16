function onQueryKeypress(event, book)
{
  if(event.keyCode == KeyEvent.DOM_VK_ENTER || event.keyCode == KeyEvent.DOM_VK_RETURN)
  {
    var text = event.target;
    var query = text.value;

    document.location.href = "searchfrm.xul.php?book=" + book + "&query=" + encodeURIComponent(query);
  }
}

function onSearchSelect(event, book)
{
  var list = event.target;
  var link = list.value;

  parent.content.location.href = "page.php/" + book + "/" + link;
}
