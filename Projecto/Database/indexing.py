from sqlite3 import connect
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.corpus import stopwords
from pprint import pprint
from string import lower, punctuation

class Document:

	def __init__(self):
		self.tokens = []
		self.postags = []

def index():
	database = connect('database.db')
	documents = []

	### GET DATABASE DATA
	for row in database.execute('SELECT doc_id, doc_datetime, doc_title, doc_description, doc_text,'+\
		' tpc_name FROM documents, topics WHERE tpc_id = doc_topic and doc_processed = 0;'):
		documents.append(Document())
		documents[-1].id = row[0]
		documents[-1].datetime = str(row[1])
		documents[-1].title = str(row[2])
		documents[-1].description = str(row[3])
		documents[-1].text = str(row[4])
		documents[-1].topic = str(row[5])

	### GET TOKENS
	for document in documents[0:1]:
		[document.tokens.append([t for t in word_tokenize(s)]) for s in sent_tokenize(document.text)]

	### GET TAGS & ENTITIES
	punct = list(punctuation)+['``','\'\'','...']
	remove_list = ['POS','PRP','PRP$','IN','TO','CC','DT']
	for document in documents[0:1]:
		[document.postags.extend(pos_tag(sentence)) for sentence in document.tokens]
		document.entities =	[c for c in ne_chunk(document.postags, binary=True) if hasattr(c, '_label')]
		document.entities = list(set([' '.join([l[0] for l in e.leaves()]) for e in document.entities]))
		document.postags = [t for t in document.postags if t[0] not in (stopwords.words('english') and punct) and t[1] not in remove_list]
		print(document.postags)
	### GET TAGS
	#for document in documents[0:1]:
	#	document.tags = pos_tag(map(lower, document.tokens))
	
	#pprint(documents[0].tags)


	#punct = list(punctuation)+['``','\'\'','...']
	#document.tokens = [t for t in document.tokens if t not in stopwords.words('english')]
	#document.tokens = [t for t in document.tokens if t not in (stopwords.words('english') and punct)]

if __name__ == "__main__":
	index()
