from gensim.models.ldamodel import LdaModel
from gensim.models import TfidfModel
from gensim import similarities
from gensim.corpora import Dictionary
from cPickle import load
from pprint import pprint
from sys import argv

class MyCorpus(object):
	def __iter__(self):
		f=open("TopicMod/terms.dat","rb")
		total=load(f)
		for i in range(total):
			yield dictionary.doc2bow(load(f))

class MyDictionary(object):
	def __iter__(self):
		f=open("TopicMod/terms.dat","rb")
		total=load(f)
		for i in range(total):
			yield load(f)

<<<<<<< HEAD
=======
class MyNewCorpus(object):
	def __iter__(self):
		f=open("TopicMod/new_terms.dat","rb")
		total=load(f)
		for i in range(total):
			yield dictionary.doc2bow(load(f))

class MyNewDictionary(object):
	def __iter__(self):
		f=open("TopicMod/new_terms.dat","rb")
		total=load(f)
		for i in range(total):
			yield load(f)


>>>>>>> 74ebeffa75b0f654abdaf4fc817d657b9f423773
def get_similar(doc):		
	def fetch_dict():
		print "Fetching Dictionary...",
		try:
			dictionary=Dictionary().load("TopicMod/dic.tm")
			print "Dictionary loaded!"
		except IOError:
			print "Dictionary not found, building Dictionary..."
			dictionary=Dictionary(i for i in MyDictionary())
			once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
			dictionary.filter_tokens(once_ids)
			dictionary.compactify() 
			print "\rDictionary Built!"
			print dictionary
			dictionary.save("TopicMod/dic.tm")
		return dictionary

	def fetch_model():
		print "Fetching LDA Model... ",
		try:
			lda = LdaModel.load('TopicMod/lda.tm')
			print "LDA Model loaded!"
		except IOError:
			print "Model not found, building LDA..."
			corpus=MyCorpus()
			#lda = LdaModel(corpus,num_topics=50,update_every=1,chunksize=1000,passes=15)
			lda = LdaModel(corpus,num_topics=50,id2word=dictionary,update_every=1,chunksize=1000,passes=50)
			print "LDA Built!"
			lda.save('TopicMod/lda.tm')
		return lda

	def fetch_index(lda):
		print "Fetching Indexes...   ",
		try:
			index = similarities.MatrixSimilarity.load('TopicMod/index.tm')
			print "Indexes loaded!"
		except IOError:
			print "Indexes not found, building Indexes..."
			corp=[i for i in corpus]

			#pprint(sorted(lda.print_topics(50),reverse=True))
			index = similarities.MatrixSimilarity(lda[corp])
			print "Indexes Built!"
			index.save('TopicMod/index.tm')
		
		return index

	global dictionary
	dictionary = fetch_dict()
	lda        = fetch_model()
	corpus     = MyCorpus()
	index      = fetch_index(lda)

	vec_bow = dictionary.doc2bow(doc)
	vec_lda = lda[vec_bow] # convert the query to LSI 
	sims=index[vec_lda]
	
	return sorted(enumerate(sims),key=lambda item: -item[1])[:10]
	#return lda[dictionary.doc2bow(doc)]

<<<<<<< HEAD
=======
def update_lda():
	def fetch_dict():
		print "Fetching Dictionary...",
		try:
			dictionary=Dictionary().load("TopicMod/dic.tm")
			print "Dictionary loaded!"
			docs=[i for i in MyNewDictionary()]
			dictionary.add_documents(docs)
			once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
			dictionary.filter_tokens(once_ids)
			dictionary.compactify() 
			print "\rDictionary Built!"
			print dictionary
			dictionary.save("TopicMod/new_dic.tm")
		except IOError:
			return -1
		return dictionary

	def fetch_model():
		print "Fetching LDA Model... ",
		try:
			lda = LdaModel.load('TopicMod/lda.tm')
			print "LDA Model loaded!"
			corpus=MyNewCorpus()
			lda.update(corpus,update_every=1,chunksize=50,passes=15)
			print "LDA Built!"
			lda.save('TopicMod/new_lda.tm')
		except IOError:
			return -1
		return lda

	global dictionary
	dictionary = fetch_dict()
	lda        = fetch_model()
	print lda.print_topics()
>>>>>>> 74ebeffa75b0f654abdaf4fc817d657b9f423773

if __name__ == '__main__':
	print get_similar(argv[1])


	
