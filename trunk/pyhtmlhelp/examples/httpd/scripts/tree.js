// tree.js
//
// Description:
// 
//   Script for controlling an expandable tree in HTML.
//
// See also:
//
//   http://www.oreillynet.com/pub/a/javascript/2002/02/22/hierarchical_menus.html
//   http://wsabstract.com/script/cut51.shtml
// 
// Author:
//
//   José Fonseca


function toggle(e) {
	parentNode = e.target;
	if ( parentNode.className == 'closed') {
		parentNode.className = 'open';
		for(i = 0; i < parentNode.childNodes.length; i++) {
			if ( parentNode.childNodes.item(i).className == 'closed')
				parentNode.childNodes.item(i).className = 'open';
		}
	} else if ( parentNode.className == 'open') {
		parentNode.className = 'closed';
		for(i = 0; i < parentNode.childNodes.length; i++) {
			if ( parentNode.childNodes.item(i).className == 'open')
				parentNode.childNodes.item(i).className = 'closed';
		}
	}
}

document.onclick = toggle;


