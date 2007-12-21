# sed script to aid the generation of .devhelp from w3c specifications

/<h2><a name="contents">Table of contents<\/a><\/h2>/,/<hr>/!d

/[^>]$/N
/[^>]$/N
s/\n/ /g

s/&nbsp;/	/g
s/\s*<br>//g

s:\s*\(\S\+\)\s*<a href="\([^"]*\)">\([^<>]*\)</a>:<sub name="\1 \3" link="\2"/>:g

