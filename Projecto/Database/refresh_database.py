from bs4 import BeautifulSoup
from urllib import urlopen
from pprint import pprint
from re import compile as rcompile, sub as rsub
from sys import exit
from nltk.tokenize import sent_tokenize
from sqlite3 import connect
from datetime import datetime
from time import sleep
from dateutil import parser

database = connect('database.db')

topics = [[field[0],str(field[1])] for field in database.execute('SELECT * FROM topics;')]
feeds = [[field[0],str(field[1])] for field in database.execute('SELECT f_topic, f_link FROM feeds;')]

titles_exist = [str(field[0]) for field in database.execute('SELECT n_title FROM news;')]

#pprint(topics)
#pprint(feeds)

for topic,url in feeds:

	html = urlopen(url).read()

	soup = BeautifulSoup(html)
	items = [item for item in soup.find_all('item')]
	titles = [item.title.findAll(text=True)[0] if item.title is not None and len(item.title.findAll(text=True))>0 else '' for item in items]
	descriptions = [item.description.findAll(text=True)[0] if item.description is not None and len(item.description.findAll(text=True))>0 else '' for item in items]
	links = [item.guid.findAll(text=True)[0] if item.guid is not None and len(item.guid.findAll(text=True))>0 else '' for item in items]
	dates = [item.pubdate.findAll(text=True)[0] if item.pubdate is not None and len(item.pubdate.findAll(text=True))>0 else '' for item in items]
	thumbnails = [item.findChildren('media:thumbnail',{'width':'144'})[0]['url'] if len(item.findChildren('media:thumbnail',{'width':'144'}))>0 else '' for item in items]

	titles = [title.encode('ascii', errors='ignore') for title in titles]
	descriptions = [description.encode('ascii', errors='ignore') for description in descriptions]

	for j in range(len(items)):
		
		print j

		if titles[j] not in titles_exist and \
			not (titles[j].startswith(('VIDEO','AUDIO','In pictures','Your pictures'))):

			print '-'
			titles_exist.append(titles[j])
			url = links[j]
			while True:
				try:
					html = urlopen(url).read()
					break
				except IOError:
					sleep(5)
					print'\nSLEEEEEP\n'

			soup = BeautifulSoup(html)
			title = str(soup.title)[7:-8]

			if any(i in title for i in ['BBC News','BBC History','BBC Science','BBC Consumer','BBC Arts','BBC Nature']):
				division = 'story-body'
			elif 'BBC Sport' in title:
				division = 'article'
			elif 'BBC - Capital' in title:
				division = 'description|story-body'

			if 'division' not in locals():
				print '\nDIVISION\n'
				continue

			content = [div for div in soup.find_all('div',{'class':rcompile(division)})]
			soup = BeautifulSoup(' '.join(list(map(str,content))))
			paragraphs = [par for par in soup.findAll('p')]
			soup = BeautifulSoup(' '.join(list(map(str,paragraphs))))
			[par.extract() for par in soup.findAll('p') if str(par).startswith('<p><strong>')]
			[par.extract() for par in soup.findAll('p',{'class':rcompile('disclaimer|terms')})]
			text = soup.get_text().replace('\n',' ').replace('\t',' ').replace('\r',' ')

			if text == '':
				continue

			title = title.decode('utf-8').encode('ascii', errors='ignore')
			text = text.encode('ascii', errors='ignore')

			rsub(' +',' ',text)
			text = text.strip()
			text = '\n'.join([k for k in sent_tokenize(text)])
			rsub(' +',' ',title)
			title = title.strip()
			text = title + '\n' + text

			text = text.replace('\'','\'\'')
			
			print titles[j]
			print descriptions[j]
			print links[j]
			print dates[j]
			print thumbnails[j]
			print '\n'

			titles[j] = titles[j].replace('\'','\'\'')
			descriptions[j] = descriptions[j].replace('\'','\'\'')

			date = parser.parse(dates[j])
			#print date

			#query = 'INSERT INTO news (n_datetime, n_link, n_thumbnail, n_title, n_description,'+\
			#	' n_text, n_topic) VALUES (\''+str(date)+'\',\''+links[j]+'\',\''+thumbnails[j]+'\',\''+\
			#	titles[j]+'\',\''+descriptions[j]+'\',\''+text+'\','+str(topic)+');'
			#print query

			database.execute('INSERT INTO news (n_datetime, n_link, n_thumbnail, n_title, n_description,'+\
				' n_text, n_topic) VALUES (\''+str(date)+'\',\''+links[j]+'\',\''+thumbnails[j]+'\',\''+\
				titles[j]+'\',\''+descriptions[j]+'\',\''+text+'\','+str(topic)+');')

			database.commit()
