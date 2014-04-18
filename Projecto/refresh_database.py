from bs4 import BeautifulSoup
import urllib
from pprint import pprint
import re
from sys import exit
import nltk

feeds = {
'Business': 'http://feeds.bbci.co.uk/news/business/rss.xml',
'Politics': 'http://feeds.bbci.co.uk/news/politics/rss.xml',
'Health': 'http://feeds.bbci.co.uk/news/health/rss.xml',
'Education': 'http://feeds.bbci.co.uk/news/education/rss.xml',
'Science & Environment': 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
'Technology': 'http://feeds.bbci.co.uk/news/technology/rss.xml',
'Entertainment & Arts': 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
'Magazine': 'http://feeds.bbci.co.uk/news/magazine/rss.xml',
'History': 'http://www.bbc.co.uk/history/0/rss.xml',
'Science & Environment': 'http://www.bbc.co.uk/science/0/rss.xml',
'Consumer': 'http://www.bbc.co.uk/consumer/rss.xml',
'Arts & Culture': 'http://www.bbc.co.uk/arts/0/rss.xml',
'Nature': 'http://feeds.bbci.co.uk/nature/rss.xml',
'Sports': 'http://feeds.bbci.co.uk/sport/0/rss.xml',
'Capital': 'http://www.bbc.com/capital/feed.rss'
}

for topic,url in feeds.iteritems():

	#url = 'http://feeds.bbci.co.uk/sport/0/rss.xml'
	html = urllib.urlopen(url).read()

	soup = BeautifulSoup(html)
	items = [item for item in soup.find_all('item')]
	soup = BeautifulSoup(' '.join(list(map(str,items))))
	titles = [i.findAll(text=True)[0] if len(i.findAll(text=True)) > 0 else '' for i in soup.findAll('title')]
	descriptions = [i.findAll(text=True)[0] if len(i.findAll(text=True)) > 0 else '' for i in soup.findAll('description')]
	links = [i.findAll(text=True)[0] if len(i.findAll(text=True)) > 0 else '' for i in soup.findAll('guid')]
	dates = [i.findAll(text=True)[0] if len(i.findAll(text=True)) > 0 else '' for i in soup.findAll('pubdate')]
	thumbnails = [i['url'] for i in soup.findAll('media:thumbnail') if i['width'] == '144']

	for j in range(len(titles)):
		if not (titles[j].startswith('VIDEO') or titles[j].startswith('In pictures:') or titles[j].startswith('Your pictures:')):
			url = links[j]
			html = urllib.urlopen(url).read()

			soup = BeautifulSoup(html)
			title = str(soup.title)[7:-8]

			if any(i in title for i in ['BBC News','BBC History','BBC Science','BBC Consumer','BBC Arts','BBC Nature']):
				division = 'story-body'
			elif 'BBC Sport' in title:
				division = 'article'
			elif 'BBC - Capital' in title:
				division = 'description|story-body'

			content = [div for div in soup.find_all('div',{"class":re.compile(division)})]
			soup = BeautifulSoup(' '.join(list(map(str,content))))
			paragraphs = [par for par in soup.findAll('p')]
			soup = BeautifulSoup(' '.join(list(map(str,paragraphs))))
			[par.extract() for par in soup.findAll('p') if str(par).startswith('<p><strong>')]
			[par.extract() for par in soup.findAll('p',{"class":re.compile('disclaimer|terms')})]
			text = soup.get_text().replace('\n',' ').replace('\t',' ').replace('\r',' ')

			while '  ' in text:
				text = text.replace('  ',' ')
			if text[0] == ' ':
				text = text[1:]

			if text != '':
				print title
				#print text
				sentences = [k for k in nltk.tokenize.sent_tokenize(text)]
				for sentence in sentences:
					print sentence

