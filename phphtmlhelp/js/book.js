function goBack(event)
{
	self.content.history.back();
	return true;
}

function goForward(event)
{
	self.content.history.forward();
	return true;
}

function goHome(event, book)
{
	self.content.location.href = "page.php/" + book + "/";
	return true;
}

function print()
{
	try
	{
		_content.print();
	}
	catch (e)
	{
	}
}
