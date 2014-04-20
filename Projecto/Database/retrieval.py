from sqlite3 import connect
from pprint import pprint
from urllib import urlopen
from bs4 import BeautifulSoup
from time import sleep
from re import compile as rcompile, sub as rsub
from nltk.tokenize import sent_tokenize
from dateutil import parser
from termcolor import cprint

class Retrieval:

	def __init__(self, indexes,updates):
		self.database = connect('database.db')
		self.get_database_data()
		self.get_rss_info()
		self.get_documents(indexes,updates)

	def get_database_data(self):
		self.topics, self.feeds, self.documents = [[],[],[]]
		for row in self.database.execute('SELECT * FROM topics;'):
			self.topics.append([row[0], str(row[1])])
		for row in self.database.execute('SELECT fds_topic, fds_link FROM feeds;'):
			self.feeds.append([row[0],str(row[1])])		
		for row in self.database.execute('SELECT doc_id, doc_datetime, doc_link FROM documents'):
			self.documents.append([row[0],str(row[1]),str(row[2])])
		#pprint(self.topics)
		#pprint(self.feeds)
		#pprint(self.documents)

	def get_rss_info(self):
		self.titles, self.descriptions, self.links, self.datetimes = [[],[],[],[]]
		self.thumbnails, self.doc_topics = [[],[]]
		for topic, link in self.feeds:
			html = urlopen(link).read()
			soup = BeautifulSoup(html)
			items = [item for item in soup.find_all('item')]
			for item in items:
				self.doc_topics.append(topic)
				if item.title is not None:
					title = item.title.findAll(text=True)
					if len(title) == 1: self.titles.append(title[0].encode('ascii',errors='ignore'))
					else:               self.titles.append('')
				if item.description is not None:
					desc = item.description.findAll(text=True)
					if len(desc) == 1: self.descriptions.append(desc[0].encode('ascii',errors='ignore'))
					else:              self.descriptions.append('')
				if item.guid is not None:
					link = item.guid.findAll(text=True)
					if len(link) == 1: self.links.append(link[0].encode('ascii',errors='ignore'))
					else:              self.links.append('')
				if item.pubdate is not None:
					date = item.pubdate.findAll(text=True)
					if len(date) == 1: self.datetimes.append(date[0].encode('ascii',errors='ignore'))
					else:              self.datetimes.append('')
				thumb = item.findChildren('media:thumbnail',{'width':'144'})
				if len(thumb) == 1: self.thumbnails.append(thumb[0]['url'].encode('ascii',errors='ignore'))
				else:               self.thumbnails.append('')

	def get_documents(self, indexes,updates):
		for index in range(len(self.titles)):
			print('('+str(index+1).ljust(4) + str(self.doc_topics[index]).ljust(3) + ')'),
			
			datetime = parser.parse(self.datetimes[index])
			try:
				pos = [doc[2] for doc in self.documents].index(self.links[index])
				if str(datetime) == str(self.documents[pos][1]):
					cprint('Unchanged Article','white',end='\n\b')
					continue
				refresh = 1
			except:
				refresh = 0

			not_article = ('VIDEO','AUDIO','In pictures','Your pictures')
			if self.titles[index].startswith(not_article):
				cprint('Not an Article','yellow',end='\n\b')
				continue

			html = urlopen(self.links[index]).read()
			soup = BeautifulSoup(html)
			title = str(soup.title)[7:-8].decode('utf-8').encode('ascii',errors='ignore')

			temp = ['BBC News','BBC History','BBC Science','BBC Consumer','BBC Arts','BBC Nature']
			if any(i in title for i in temp): division = 'story-body'
			elif 'BBC Sport' in title:        division = 'article'
			elif 'BBC - Capital' in title:    division = 'description|story-body'
			else:                             cprint('Website not known','red',end='\n\b'); continue

			content = [div for div in soup.find_all('div',{'class':rcompile(division)})]
			soup = BeautifulSoup(' '.join(list(map(str,content))))
			paragraphs = [p for p in soup.findAll('p')]
			soup = BeautifulSoup(' '.join(list(map(str,paragraphs))))
			[p.extract() for p in soup.findAll('p') if str(p).startswith('<p><strong>')]
			[p.extract() for p in soup.findAll('p',{'class':rcompile('disclaimer|terms')})]

			text = soup.get_text().replace('\n',' ').replace('\t',' ').replace('\r',' ')
			text = text.encode('ascii', errors='ignore')
			if text == '':
				cprint('Empty Text','yellow',end='\n\b')
				continue

			rsub(' +',' ',text)
			text = text.strip()
			text = '\n'.join([sentence for sentence in sent_tokenize(text)])
			title = title.split('-')[-1]
			rsub(' +',' ',title)
			title = title.strip()
			text = title + '\n' + text

			if refresh == 1:
				self.database.execute('UPDATE documents SET doc_datetime = \''+str(datetime)+'\','+\
					' doc_thumbnail = \''+self.thumbnails[index]+'\','+\
					' doc_title = \''+self.titles[index].replace('\'','\'\'')+'\','+\
					' doc_description = \''+self.descriptions[index].replace('\'','\'\'')+'\','+\
					' doc_text = \''+text.replace('\'','\'\'')+'\''+\
					' WHERE doc_link = \''+self.links[index]+'\';')
				cprint('Update - '+self.titles[index],'cyan',attrs=['bold'],end='\n\b')
				updates.append(index+1)
			else:
				self.documents.append([len(self.documents), self.titles[index], datetime])
				self.database.execute('INSERT INTO documents (doc_datetime, doc_link, doc_thumbnail,'+\
					' doc_title, doc_description, doc_text, doc_topic) VALUES (\''+\
					str(datetime)+'\',\''+self.links[index]+'\',\''+self.thumbnails[index]+'\',\''+\
					self.titles[index].replace('\'','\'\'')+'\',\''+\
					self.descriptions[index].replace('\'','\'\'')+'\',\''+\
					text.replace('\'','\'\'')+'\','+str(self.doc_topics[index])+');')
				cprint('Insert - '+self.titles[index],'green',attrs=['bold'],end='\n\b')
				indexes.append(index+1)

			self.database.commit()


if __name__ == "__main__":
	indexes = []
	updates = []
	Retrieval(indexes,updates)
	print len(indexes),'-',indexes
	print len(updates),'-',updates
