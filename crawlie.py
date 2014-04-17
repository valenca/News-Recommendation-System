from feedparser import parse as feedparse
from urllib import urlopen
from pprint import pprint

target = 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml'
feed   = feedparse(target)
links   = [feed['feed']['links'][i]['href'] for i in range(len(feed['feed']['links']))]

for link in links:
	url=urlopen(link)
	raw=url.read()
	break

pprint(raw)






















