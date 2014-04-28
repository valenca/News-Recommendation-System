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
from cPickle import load, dump
from nltk.classify import DecisionTreeClassifier
import os.path

class Document:
	def __init__(self):
		self.topics = []
		self.tokens = {'title':[],'desc':[],'text':[]}
		self.postags = {'title':[],'desc':[],'text':[]}
		self.entities = {}
		self.terms = {'title':[],'desc':[],'text':[]}


class Database:
	def __init__(self):
		self.database = connect('../Database/database.db')

	def get_ntopics(self):
		for row in self.database.execute('SELECT count(*) FROM topics;'):
			return row[0]

	def get_data(self):
		documents = []
		for row in self.database.execute('SELECT doc_id, doc_datetime, doc_title, doc_description,'+\
			' doc_text FROM documents WHERE doc_processed = 0;'):
			documents.append(Document())
			documents[-1].id = row[0]
			documents[-1].datetime = str(row[1])
			documents[-1].title = str(row[2])
			documents[-1].description = str(row[3])
			documents[-1].text = str(row[4])
			for row2 in self.database.execute('SELECT tpc_id, tpc_name FROM topics, tpc_doc WHERE '+\
				' tpd_document = '+str(row[0])+' AND tpc_id = tpd_topic;'):
				documents[-1].topics.append([row2[0], str(row2[1])])
		return documents

	def update(self, doc):
		self.database.execute('UPDATE documents SET doc_processed = 1 WHERE doc_id = '+str(doc.id)+';')
		self.database.commit()


class TextMining:
	def __init__(self):
		self.punct = list(punctuation)+['``','\'\'','...']
		self.remove_list = ['POS','PRP','PRP$','IN','TO','CC','DT','EX','LS','PDT','RP','UH']
		self.replace_list = {'\'s':'is','\'re':'are','\'m':'am','\'ll':'will','\'ve':'have','n\'t':'not',
			'\'d':'had'}
		self.lemmatizer = wordnet.WordNetLemmatizer()

	def tokens(self, doc):
		[doc.tokens['title'].append([t for t in word_tokenize(s)]) for s in sent_tokenize(doc.title)]
		[doc.tokens['desc'].append([t for t in word_tokenize(s)]) for s in sent_tokenize(doc.description)]
		[doc.tokens['text'].append([t for t in word_tokenize(s)]) for s in sent_tokenize(doc.text)]

	def postags_entities(self, doc):
		for f in ['title', 'desc', 'text']:
			[doc.postags[f].extend(pos_tag(sentence)) for sentence in doc.tokens[f]]
			doc.entities[f] = [c for c in ne_chunk(doc.postags[f], binary=True) if hasattr(c, '_label')]
			doc.entities[f] = list(set([' '.join([l[0] for l in e.leaves()]) for e in doc.entities[f]]))
			doc.postags[f] = [(self.replace_list[t[0]], t[1]) if t[0] in self.replace_list.keys()
			    else (t[0], t[1]) for t in doc.postags[f]]
			doc.postags[f] = [t for t in doc.postags[f] if t[0] not in (stopwords.words('english') \
				and self.punct) and t[1] not in self.remove_list]
	def terms(self, doc):
		for f in ['title', 'desc', 'text']:
			doc.terms[f] = [lower(t[0]) if t[0] not in doc.entities[f] else t[0] for t in doc.postags[f]]
			doc.terms[f] = [str(self.lemmatizer.lemmatize(t)) for t in doc.terms[f]]
			doc.terms[f] = list(map(lower,doc.terms[f]))


class Index:
	def __init__(self):		
		if not os.path.isdir('Index'):
			os.mkdir('Index')
			schema = Schema(id=NUMERIC(stored=True,unique=True),
							datetime=DATETIME,
							title=TEXT(field_boost=20),
							description=TEXT(field_boost=10),
							text=TEXT(field_boost=6),
							topics=TEXT(field_boost=3))
			create_in('Index', schema)
		self.index = open_dir('Index')

	def index(self, doc):
		writer = self.index.writer()
		writer.update_document(id = doc.id, datetime = parser.parse(doc.datetime), title = doc.terms['title'],
			                   description = doc.terms['desc'], text = doc.terms['text'],
			                   topics = list(map(unicode,list(map(lower,[t[1] for t in doc.topics])))))
		writer.commit()

	def optimize(self):
		print('Optimizing ...')
		self.index.optimize()

class Tags:

	def __init__(self):
		pass

	def get_tags(self, doc):
		pass

class Themes:

	def __init__(self):
		if not os.path.isfile('training.info'):
			self.info = []
		else:
			with open('training.info', 'rb') as f:
				self.info = load(f)

	def insert(self, doc):
		data = doc.terms['title'] + doc.terms['desc'] + doc.terms['text'] + [[t[0] for t in doc.topics]]
		if len(self.info) >= doc.id:
			self.info[doc.id-1] = data
		else:
			self.info.append(data)

	def write(self):
		with open('training.info', 'wb') as f:
			dump(self.info, f)

	def train(self, ntopics):
		all_terms = []
		[all_terms.extend(i[:-1]) for i in self.info]
		all_terms = list(set(all_terms))
		hashmap = []
		[hashmap.append([1 if t in i[:-1] else 0 for t in all_terms]) for i in self.info]

		self.sets = [[] for i in range(ntopics)]
		for i in range(ntopics):
			for j in range(len(self.info)):
				if i+1 in self.info[j][-1]: v = 1
				else:                       v = 0
				self.sets[i].append((dict(zip(all_terms,hashmap[j])),v))

		self.classifiers = [DecisionTreeClassifier.train(s) for s in self.sets]

	def test(self, doc):
		return [c.batch_classify([self.sets[0][doc.id-1][0]])[0] for c in self.classifiers]

if __name__ == '__main__':
	database = Database()
	tm = TextMining()
	index = Index()
	themes = Themes()
	ntopics = database.get_ntopics()
	documents = database.get_data()
	for n,doc in enumerate(documents[0:1]):
		print('(' + str(n+1) + ' ' + str(doc.id) + ')')
		tm.tokens(doc)
		tm.postags_entities(doc)
		tm.terms(doc)
		themes.insert(doc)
	#	index.index(doc)
	#	database.update(doc)
	#themes.write()
	themes.train(ntopics)
	for n,doc in enumerate(documents[0:1]):
		print themes.test(doc)
	#index.optimize()