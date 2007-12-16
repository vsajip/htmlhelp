import sys

enc = 'UTF-8'

letter = ''
digit = ''
space = ''
upper = ''
lower = ''


for i in range(0, 0x2000):
	si = unichr(i)
	sj = si.lower()
	j = ord(sj)

	if i <= 32 or i >= 128:
		xi = '\\x%02X' % i
	else:
		xi = chr(i)
	if j <= 32 or j >= 128:
		xj = '\\x%02X' % j
	else:
		xj = chr(j)

	if i != j:
		upper += xi
		lower += xj
	
	if si.isalpha():
		letter += xi
	if si.isdigit():
		digit += xi
	if si.isspace():
		space += xi


print 'letter = "%s";' % letter
print 'digit = "%s";' % digit
print 'space = "%s";' % space
print 'upper = "%s";' % upper
print 'lower = "%s";' % lower

sys.exit()
l = {
	'ASCII': 0x80,
	'ISO-8859-1': 0x100,
	'ISO-8859-15': 0x100,
	'UTF-8': 0x11000,
}

for i in range(0, 256):
	si = chr(i).decode(enc)
	sj = si.lower()
	j = ord(sj.encode(enc))

	if i <= 32 or i >= 128:
		xi = '\\x%02X' % i
	else:
		xi = chr(i)
	if j <= 32 or j >= 128:
		xj = '\\x%02X' % j
	else:
		xj = chr(j)

	if i != j:
		upper += xi
		lower += xj
	
	if si.isalpha():
		letter += xi
	if si.isdigit():
		digit += xi
	if si.isspace():
		space += xi
		

print 'letter = "%s";' % letter
print 'digit = "%s";' % digit
print 'space = "%s";' % space
print 'upper = "%s";' % upper
print 'lower = "%s";' % lower

