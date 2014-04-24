from sqlite3 import connect
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.corpus import stopwords
from nltk.stem import wordnet
from pprint import pprint
from string import lower, punctuation
from whoosh.fields import Schema, NUMERIC, DATETIME, TEXT
from whoosh.index import create_in, open_dir
from dateutil import parser
import os.path

class Document:

	def __init__(self):
		self.topics = []
		self.tokens = {'title':[],'desc':[],'text':[]}
		self.postags = {'title':[],'desc':[],'text':[]}
		self.entities = {}
		self.terms = {'title':[],'desc':[],'text':[]}

def index():
	database = connect('database.db')
	documents = []
	if not os.path.isdir("Index"):
		os.mkdir("Index")
		schema = Schema(id=NUMERIC(stored=True,unique=True),
						datetime=DATETIME,
						title=TEXT(field_boost=20),
						description=TEXT(field_boost=10),
						text=TEXT(field_boost=6),
						topic=TEXT(field_boost=3))
		create_in('Index', schema)
	index = open_dir('Index')

	### GET DATABASE DATA
	for row in database.execute('SELECT doc_id, doc_datetime, doc_title, doc_description, doc_text'+\
		' FROM documents WHERE doc_processed = 0;'):
		documents.append(Document())
		documents[-1].id = row[0]
		documents[-1].datetime = str(row[1])
		documents[-1].title = str(row[2])
		documents[-1].description = str(row[3])
		documents[-1].text = str(row[4])
		for row2 in database.execute('SELECT tpc_name FROM topics, tpc_doc WHERE tpd_document = '+\
			str(row[0])+' AND tpc_id = tpd_topic;'):
			documents[-1].topics.append((str(row2[0])))

	punct = list(punctuation)+['``','\'\'','...']
	remove_list = ['POS','PRP','PRP$','IN','TO','CC','DT','EX','LS','PDT','RP','UH']
	replace_list = {'\'s':'is','\'re':'are','\'m':'am','\'ll':'will','\'ve':'have','n\'t':'not'}
	lemmatizer = wordnet.WordNetLemmatizer()

	print(len(documents))
	for n,doc in enumerate(documents):
		print('(' + str(n+1) + ' ' + str(doc.id) + ')')

		### GET TOKENS
		[doc.tokens['title'].append([t for t in word_tokenize(s)]) for s in sent_tokenize(doc.title)]
		[doc.tokens['desc'].append([t for t in word_tokenize(s)]) for s in sent_tokenize(doc.description)]
		[doc.tokens['text'].append([t for t in word_tokenize(s)]) for s in sent_tokenize(doc.text)]

		### GET TAGS & ENTITIES
		for f in ['title', 'desc', 'text']:
			[doc.postags[f].extend(pos_tag(sentence)) for sentence in doc.tokens[f]]
			doc.entities[f] = [c for c in ne_chunk(doc.postags[f], binary=True) if hasattr(c, '_label')]
			doc.entities[f] = list(set([' '.join([l[0] for l in e.leaves()]) for e in doc.entities[f]]))
			doc.postags[f] = [t for t in doc.postags[f] if t[0] not in (stopwords.words('english') and punct)\
			                                               and t[1] not in remove_list]

		### GET TERMS
		for f in ['title', 'desc', 'text']:
			for postag in doc.postags[f]:
				try:    doc.terms[f].append(replace_list[postag[0]])
				except: doc.terms[f].append(postag[0])
			doc.terms[f] = [lower(t) if t not in doc.entities[f] else t for t in doc.terms[f]]
			doc.terms[f] = [str(lemmatizer.lemmatize(t)) for t in doc.terms[f]]

		### INDEX DOCUMENT
		writer = index.writer()
		writer.update_document(id = doc.id,
			                   datetime = parser.parse(doc.datetime),
			                   title = doc.terms['title'],
			                   description = doc.terms['desc'],
			                   text = doc.terms['text'],
			                   topic = list(map(unicode,list(map(lower,doc.topics)))))
		writer.commit()

		### UPDATE DB
		database.execute('UPDATE documents SET doc_processed = 1 WHERE doc_id = '+str(doc.id)+';')
		database.commit()

	print('Optimizing ...')
	index.optimize()

if __name__ == "__main__":
	index()
