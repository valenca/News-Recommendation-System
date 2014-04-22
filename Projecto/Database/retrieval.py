from sqlite3 import connect
from urllib import urlopen
from bs4 import BeautifulSoup
from re import compile as rcompile, sub as rsub
from nltk.tokenize import sent_tokenize
from dateutil import parser

def retrieve():
	database = connect('database.db')
	topics,feeds,documents,titles,descriptions = [[],[],[],[],[]]
	links,datetimes,thumbnails,doc_topics = [[],[],[],[]]

	### GET DATABASE DATA
	for row in database.execute('SELECT * FROM topics;'):
		topics.append([row[0], str(row[1])])
	for row in database.execute('SELECT fds_topic, fds_link FROM feeds;'):
		feeds.append([row[0],str(row[1])])		
	for row in database.execute('SELECT doc_id, doc_datetime, doc_link FROM documents'):
		documents.append([row[0],str(row[1]),str(row[2])])

<<<<<<< HEAD
	### GET RSS INFO
	for topic, link in feeds:
		html = urlopen(link).read()
		soup = BeautifulSoup(html)
		items = [item for item in soup.find_all('item')]
		for item in items:
			doc_topics.append(topic)
			if item.title is not None:
				title = item.title.findAll(text=True)
				if len(title) == 1: titles.append(title[0].encode('ascii',errors='ignore'))
				else:               titles.append('')
			if item.description is not None:
				desc = item.description.findAll(text=True)
				if len(desc) == 1: descriptions.append(desc[0].encode('ascii',errors='ignore'))
				else:              descriptions.append('')
			if item.guid is not None:
				link = item.guid.findAll(text=True)
				if len(link) == 1: links.append(link[0].encode('ascii',errors='ignore'))
				else:              links.append('')
			if item.pubdate is not None:
				date = item.pubdate.findAll(text=True)
				if len(date) == 1: datetimes.append(date[0].encode('ascii',errors='ignore'))
				else:              datetimes.append('')
			thumb = item.findChildren('media:thumbnail',{'width':'144'})
			if len(thumb) == 1: thumbnails.append(thumb[0]['url'].encode('ascii',errors='ignore'))
			else:               thumbnails.append('')
=======
	def get_documents():
		new = 0
		updated = 0
		for index in range(len(titles)):
			print('('+str(index+1).ljust(4) + str(doc_topics[index]).ljust(2) + ')'),
			
			datetime = parser.parse(datetimes[index])
			try:
				pos = [doc[2] for doc in documents].index(links[index])
				if str(datetime) == str(documents[pos][1]):
					print('Unchanged Article')
					continue
				refresh = 1
			except:
				refresh = 0
>>>>>>> a7cbd74a8d9f40b0ab24868de33bf699acaba188

	### GET DOCUMENTS
	new = 0
	updated = 0
	for index in range(len(titles)):
		print('('+str(index+1).ljust(4) + str(doc_topics[index]).ljust(2) + ')'),
		
		datetime = parser.parse(datetimes[index])
		try:
			pos = [doc[2] for doc in documents].index(links[index])
			if str(datetime) == str(documents[pos][1]):
				print('Unchanged Article')
				continue
			refresh = 1
		except:
			refresh = 0

		not_article = ('VIDEO','AUDIO','In pictures','Your pictures')
		if titles[index].startswith(not_article):
			print('Not an Article')
			continue

		html = urlopen(links[index]).read()
		soup = BeautifulSoup(html)
		title = str(soup.title)[7:-8].decode('utf-8').encode('ascii',errors='ignore')

		temp = ['BBC News','BBC History','BBC Science','BBC Consumer','BBC Arts','BBC Nature']
		if any(i in title for i in temp): division = 'story-body'
		elif 'BBC Sport' in title:        division = 'article'
		elif 'BBC - Capital' in title:    division = 'description|story-body'
		else:                             print('Website not known'); continue

		content = [div for div in soup.find_all('div',{'class':rcompile(division)})]
		soup = BeautifulSoup(' '.join(list(map(str,content))))
		paragraphs = [p for p in soup.findAll('p')]
		soup = BeautifulSoup(' '.join(list(map(str,paragraphs))))
		[p.extract() for p in soup.findAll('p') if str(p).startswith('<p><strong>')]
		[p.extract() for p in soup.findAll('p',{'class':rcompile('disclaimer|terms')})]

		text = soup.get_text().replace('\n',' ').replace('\t',' ').replace('\r',' ')
		text = text.encode('ascii', errors='ignore')
		if text == '':
			print('Empty Text')
			continue

<<<<<<< HEAD
		rsub(' +',' ',text)
		text = text.strip()
		text = '\n'.join([sentence for sentence in sent_tokenize(text)])
		title = title.split('-')[-1]
		rsub(' +',' ',title)
		title = title.strip()
		text = title + '\n' + text

		if refresh == 1:
			database.execute('UPDATE documents SET doc_processed = 0,'+
				' doc_datetime = \''+str(datetime)+'\','+\
				' doc_thumbnail = \''+thumbnails[index]+'\','+\
				' doc_title = \''+titles[index].replace('\'','\'\'')+'\','+\
				' doc_description = \''+descriptions[index].replace('\'','\'\'')+'\','+\
				' doc_text = \''+text.replace('\'','\'\'')+'\''+\
				' WHERE doc_link = \''+links[index]+'\';')
			print('Update - '+titles[index])
			updated += 1
		else:
			documents.append([len(documents), titles[index], datetime])
			database.execute('INSERT INTO documents (doc_datetime, doc_link, doc_thumbnail,'+\
				' doc_title, doc_description, doc_text, doc_topic) VALUES (\''+\
				str(datetime)+'\',\''+links[index]+'\',\''+thumbnails[index]+'\',\''+\
				titles[index].replace('\'','\'\'')+'\',\''+\
				descriptions[index].replace('\'','\'\'')+'\',\''+\
				text.replace('\'','\'\'')+'\','+str(doc_topics[index])+');')
			print('Insert - '+titles[index])
			new += 1

		database.commit()
		
	print new,"new,", updated,"updated."
=======
			if refresh == 1:
				database.execute('UPDATE documents SET doc_processed = 0,'+
					' doc_datetime = \''+str(datetime)+'\','+\
					' doc_thumbnail = \''+thumbnails[index]+'\','+\
					' doc_title = \''+titles[index].replace('\'','\'\'')+'\','+\
					' doc_description = \''+descriptions[index].replace('\'','\'\'')+'\','+\
					' doc_text = \''+text.replace('\'','\'\'')+'\''+\
					' WHERE doc_link = \''+links[index]+'\';')
				print('Update - '+titles[index])
				updated += 1
			else:
				documents.append([len(documents), titles[index], datetime])
				database.execute('INSERT INTO documents (doc_datetime, doc_link, doc_thumbnail,'+\
					' doc_title, doc_description, doc_text, doc_topic) VALUES (\''+\
					str(datetime)+'\',\''+links[index]+'\',\''+thumbnails[index]+'\',\''+\
					titles[index].replace('\'','\'\'')+'\',\''+\
					descriptions[index].replace('\'','\'\'')+'\',\''+\
					text.replace('\'','\'\'')+'\','+str(doc_topics[index])+');')
				print('Insert - '+titles[index])
				new += 1

			database.commit()
		print new,"new,", updated,"updated."
	
	database = connect('database.db')
	topics,feeds,documents,titles,descriptions = [[],[],[],[],[]]
	links,datetimes,thumbnails,doc_topics = [[],[],[],[]]
	get_database_data()
	get_rss_info()
	get_documents()
>>>>>>> a7cbd74a8d9f40b0ab24868de33bf699acaba188

if __name__ == "__main__":
	retrieve()
