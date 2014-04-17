from feedparser import parse as feedparse
from urllib import urlopen
from pprint import pprint
from bs4 import BeautifulSoup as soup

if __name__ == '__main__':
	target = 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml'
	feed   = feedparse(target)
	links   = [feed['feed']['links'][i]['href'] for i in range(len(feed['feed']['links']))]

	for link in links:
		url=urlopen(link)
		raw=url.read()
		break

	parsed = soup(raw)
	for i in parsed.body:
		print i
	#print dir(parsed.body)
	#print parsed.body.find('div', attrs={'class':'story-body'}).text
	






















