from gensim.models.ldamodel import LdaModel
from gensim.models import TfidfModel
from gensim import similarities
from gensim.corpora import Dictionary
from cPickle import load
from pprint import pprint
from sys import argv

class MyCorpus(object):
	def __iter__(self):
		f=open("Topic/terms.dat","rb")
		total=load(f)
		for i in range(total):
			yield dictionary.doc2bow(load(f))

class MyDictionary(object):
	def __iter__(self):
		f=open("Topic/terms.dat","rb")
		total=load(f)
		for i in range(total):
			yield load(f)

def get_similar(doc):		
	def fetch_dict():
		print "Fetching Dictionary...",
		try:
			dictionary=Dictionary().load("Topic/dic.tm")
			print "Dictionary loaded!"
		except IOError:
			print "Dictionary not found, building Dictionary..."
			dictionary=Dictionary(i for i in MyDictionary())
			once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
			dictionary.filter_tokens(once_ids)
			dictionary.compactify() 
			print "\rDictionary Built!"
			print dictionary
			dictionary.save("Topic/dic.tm")
		return dictionary

	def fetch_model(dictionary):
		print "Fetching LDA Model... ",
		try:
			lda = LdaModel.load('Topic/lda.tm')
			print "LDA Model loaded!"
		except IOError:
			print "Model not found, building LDA..."
			corpus=MyCorpus()
			#lda = LdaModel(corpus,num_topics=50,update_every=1,chunksize=1000,passes=15)
			lda = LdaModel(corpus,num_topics=50,id2word=dictionary,update_every=1,chunksize=1000,passes=50)
			print "LDA Built!"
			lda.save('Topic/lda.tm')
		return lda

	def fetch_index(lda):
		print "Fetching Indexes...   ",
		try:
			index = similarities.MatrixSimilarity.load('Topic/index.tm')
			print "Indexes loaded!"
		except IOError:
			print "Indexes not found, building Indexes..."
			corp=[i for i in MyCorpus()]

			#pprint(sorted(lda.print_topics(50),reverse=True))
			index = similarities.MatrixSimilarity(lda[corp])
			print "Indexes Built!"
			index.save('Topic/index.tm')
		
		return index

	global dictionary
	fetch_index(fetch_model(fetch_dict()))

	vec_bow = dictionary.doc2bow(doc)
	vec_lda = lda[vec_bow] 
	sims=index[vec_lda]
	
	return sorted(enumerate(sims),key=lambda item: -item[1])[:10]

if __name__ == '__main__':
	print get_similar(argv[1])


	
