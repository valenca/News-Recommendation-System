def gprint(string, colour='white'):
	colours = {
	'white':	255,
	'lgray':	249,
	'gray':		243,
	'dgray':	237,
	'black':	232,
	'dred':		124,
	'red':		196,
	'orange':	202,	
	'brown':	130,
	'dyellow':	214,
	'yellow':	226,
	'lgreen':	118,
	'green':	40,
	'dgreen':	28,
	'lblue':	45,
	'blue':		33,
	'dblue':	19,
	'purple':	93,
	'pink':		201
	}
	if colour in colours.keys():
		colour = colours[colour]
	else:
		colour = 255
	return '\033[38;05;' + str(colour) + 'm' + string + '\033[0m'
