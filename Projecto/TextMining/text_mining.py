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
from whoosh.analysis import StemmingAnalyzer
from dateutil import parser
from cPickle import load, dump
from nltk.classify import NaiveBayesClassifier
from collections import Counter
from sys import exit, stdout
from gensim.models.ldamodel import LdaModel
from gensim import similarities
from gensim.corpora import Dictionary
from operator import itemgetter
import os.path

class Document:
	def __init__(self):
		self.topics = []
		self.tokens = {'title':[],'desc':[],'text':[]}
		self.postags = {'title':[],'desc':[],'text':[]}
		self.entities = {}
		self.topmod = {}
		self.terms = {'title':[],'desc':[],'text':[]}


class Database:
	def __init__(self):
		self.database = connect('../Database/database.db')

	def get_documents(self):
		documents = []
		for row in self.database.execute('SELECT doc_id, doc_datetime, doc_title, doc_description,'+\
			' doc_text FROM documents WHERE doc_processed = 0;'):
			documents.append(Document())
			documents[-1].id = row[0]
			documents[-1].datetime = str(row[1])
			documents[-1].title = str(row[2])
			documents[-1].description = str(row[3])
			documents[-1].text = str(row[4])
			for row2 in self.database.execute('SELECT tpc_id, tpc_name FROM topics, tpc_doc WHERE tpd_document = '+str(row[0])+' AND tpc_id = tpd_topic;'):
				documents[-1].topics.append([row2[0], str(row2[1])])
		return documents

	def processed(self, doc):
		self.database.execute('UPDATE documents SET doc_processed = 1 WHERE doc_id = '+str(doc.id)+';')


class TextMining:
	def __init__(self):
		self.punct = list(punctuation)+['``','\'\'','...']
		self.remove_list = [['could','said','would','told','say','tell','use','used','mr','mrs'],
		                    ['POS','PRP','PRP$','IN','TO','CC','DT','EX','LS','PDT','RP','UH','CD']]
		self.replace_list = {'\'s':'is','\'re':'are','\'m':'am','\'ll':'will','\'ve':'have','n\'t':'not','\'d':'had'}
		self.topmod_list = ['NN','NNS','NNP','NNPS','VB','VBD','VBN','VBP','VBZ']
		self.lemmatizer = wordnet.WordNetLemmatizer()

	def tokens(self, doc):
		[doc.tokens['title'].append([t for t in word_tokenize(s)]) for s in sent_tokenize(doc.title)]
		[doc.tokens['desc'].append([t for t in word_tokenize(s)]) for s in sent_tokenize(doc.description)]
		[doc.tokens['text'].append([t for t in word_tokenize(s)]) for s in sent_tokenize(doc.text)]

	def postags(self, doc):
		for f in ['title', 'desc', 'text']:
			[doc.postags[f].extend(pos_tag(sentence)) for sentence in doc.tokens[f]]
			doc.entities[f] = [c for c in ne_chunk(doc.postags[f], binary=True) if hasattr(c, '_label')]
			doc.entities[f] = list(set([' '.join([l[0] for l in e.leaves()]) for e in doc.entities[f]]))
			doc.topmod[f] = [t for t in doc.postags[f] if t[1] in self.topmod_list]			
			doc.topmod[f] = [(self.replace_list[t[0]], t[1]) if t[0] in self.replace_list.keys() else (t[0], t[1]) for t in doc.topmod[f]]
			doc.topmod[f] = [t for t in doc.topmod[f] if lower(t[0]) not in stopwords.words('english')+self.punct + self.remove_list[0] and t[1] not in self.remove_list[1]]
			doc.postags[f] = [(self.replace_list[t[0]], t[1]) if t[0] in self.replace_list.keys() else (t[0], t[1]) for t in doc.postags[f]]
			doc.postags[f] = [t for t in doc.postags[f] if lower(t[0]) not in stopwords.words('english')+self.punct + self.remove_list[0] and t[1] not in self.remove_list[1]]

	def terms(self, doc):
		for f in ['title', 'desc', 'text']:
			doc.topmod[f] = [str(self.lemmatizer.lemmatize(lower(t[0]))) for t in doc.topmod[f]]
			doc.topmod[f] = [t for t in doc.topmod[f] if t not in self.remove_list[0]]
			doc.terms[f] = [lower(t[0]) if t[0] not in doc.entities[f] else t[0] for t in doc.postags[f]]
			doc.terms[f] = [str(self.lemmatizer.lemmatize(t)) for t in doc.terms[f]]
			doc.terms[f] = list(map(lower,doc.terms[f]))
			doc.terms[f] = [t for t in doc.terms[f] if t not in self.remove_list[0]]

	def write(self, database, doc):
		entities = []
		[entities.extend(e) for e in doc.entities.values()]
		entities = list(set(entities))
		for e in entities:
			database.database.execute('INSERT INTO entities VALUES ('+str(doc.id)+',\''+e.replace('\'','\'\'')+'\');')


class Index:
	def __init__(self):
		self.analyser = StemmingAnalyzer(stoplist=None)
		if not os.path.isdir('Index'):
			os.mkdir('Index')
			schema = Schema(id = NUMERIC(stored=True,unique=True),
							datetime = DATETIME,
							title = TEXT(field_boost=20),
							s_title = TEXT(stored=True,field_boost=0,analyzer=self.analyser),
							description = TEXT(field_boost=10),
							s_description = TEXT(stored=True,field_boost=0,analyzer=self.analyser),
							text = TEXT(field_boost=6),
							s_text = TEXT(stored=True,field_boost=0,analyzer=self.analyser),
							topics = TEXT(field_boost=3))
			create_in('Index', schema)
		self.index = open_dir('Index')

	def update(self, doc):
		writer = self.index.writer()
		writer.update_document(id = doc.id,
			                   datetime = parser.parse(doc.datetime),
			                   title = doc.terms['title'],
			                   s_title = unicode(doc.title),
			                   description = doc.terms['desc'],
			                   s_description = unicode(doc.description),
			                   text = doc.terms['text'],
			                   s_text = unicode(doc.text),
			                   topics = list(map(unicode,[t[1] for t in doc.topics])))
		writer.commit()

	def optimize(self):
		self.index.optimize()


class MyCorpus(object):
	def __init__(self, tm):
		self.tm = tm
	def __iter__(self):
		for key,terms in self.tm.data.iteritems():
			yield dictionary.doc2bow(terms)
class MyDictionary(object):
	def __init__(self, tm):
		self.tm = tm
	def __iter__(self):
		for key,terms in self.tm.data.iteritems():
			self.tm.translator.append(key)
			yield terms							
class TopicModelling:
	def __init__(self):
		if os.path.isfile('Topic/data.loc'):
			with open('Topic/data.loc','rb') as f:
				load(f)
				self.data = load(f)
		else:
			self.data = {}
		self.translator = []

	def update(self, doc):
		self.data[doc.id] = doc.topmod['text']

	def write(self):
		with open('Topic/data.loc','wb') as f:
			dump(len(self.data),f)
			dump(self.data,f)

		nr = []
		for v in self.data.values():
			nr.extend(v)
		c = Counter(nr).items()
		c.sort(key=itemgetter(1), reverse = True)
		nr = [i[0] for i in c if i[1] > 4 and len(i[0])> 3]
		with open('ac.loc','wb') as f:
			dump(nr,f)

	def generate_models(self):

		def fetch_dict():
			global dictionary
			dictionary=Dictionary([i for i in my_dictionary])
			once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
			dictionary.filter_tokens(once_ids)
			dictionary.compactify()
			dictionary.save("Topic/dic.loc")
			return dictionary

		def fetch_model(dictionary):
			corpus=my_corpus
			lda = LdaModel(corpus,num_topics=100,update_every=1,chunksize=1000,passes=15)
			#lda = LdaModel(corpus,num_topics=100,id2word=dictionary,update_every=1,chunksize=1000,passes=50)
			lda.save('Topic/lda.loc')
			return lda

		def fetch_index(lda):
			corp=[i for i in my_corpus]
			index = similarities.MatrixSimilarity(lda[corp])
			index.save('Topic/index.loc')

		global dictionary
		my_dictionary = MyDictionary(self)
		my_corpus = MyCorpus(self)
		fetch_index(fetch_model(fetch_dict()))
		
		with open('Topic/translator.loc', 'wb') as f:
			dump(self.translator,f)


if __name__ == '__main__':

	database = Database()
	mining = TextMining()
	index = Index()
	modelling = TopicModelling()

	documents = database.get_documents()

	total_docs = len(documents)
	line = ''

	if total_docs == 0:
		print 'No new documents'
		exit(0)

	stdout.write('\rProcessing\n'); stdout.flush()
	for n,doc in enumerate(documents):
		stdout.write('\r'+' '*len(line))
		line = ' ('+str(n+1)+'/'+str(total_docs)+') '+str(doc.id)+' - '+\
		       ' & '.join([t[1] for t in doc.topics])+' - '+doc.title
		stdout.write('\r'+line)
		stdout.flush()
		mining.tokens(doc)
		mining.postags(doc)
		mining.terms(doc)
		mining.write(database, doc)
	
	stdout.write('\r'+' '*len(line))
	stdout.write('\rIndexing\n'); stdout.flush()
	for n,doc in enumerate(documents):
		stdout.write('\r'+' '*len(line))
		line = '\r ('+str(n+1)+'/'+str(total_docs)+') '+str(doc.id)
		stdout.write('\r'+line)
		stdout.flush()
		index.update(doc)
	stdout.write('\r'+' '*len(line))
	line = '\r Optimizing ...'
	stdout.write('\r'+line)
	stdout.flush()
	index.optimize()

	stdout.write('\r'+' '*len(line))
	stdout.write('\rModelling\n'); stdout.flush()
	for n,doc in enumerate(documents):
		stdout.write('\r'+' '*len(line))
		line = '\r ('+str(n+1)+'/'+str(total_docs)+') '+str(doc.id)
		stdout.write('\r'+line)
		stdout.flush()
		modelling.update(doc)
	stdout.write('\r'+' '*len(line))
	line = '\r Generating AutoComplete Database ...'
	stdout.write('\r'+line)
	stdout.flush()
	modelling.write()
	stdout.write('\r'+' '*len(line))
	line = '\r Generating LDA Model ...'
	stdout.write('\r'+line)
	stdout.flush()
	modelling.generate_models()

	stdout.write('\r'+' '*len(line))
	stdout.write('\rDB Updating\n'); stdout.flush()
	[database.processed(doc) for doc in documents]
	database.database.commit()
