from gensim.models.ldamodel import LdaModel
from gensim.models import TfidfModel

from gensim.corpora import Dictionary

from cPickle import load
from pprint import pprint

class MyCorpus(object):
	def __iter__(self):
		f=open("terms.dat","rb")
		total=load(f)
		for i in range(total):
			yield dictionary.doc2bow(load(f))

class MyDictionary(object):
	def __iter__(self):
		f=open("terms.dat","rb")
		total=load(f)
		for i in range(total):
			yield load(f)
		
def fetch_dict():
	print "Fetching Dictionary..."
	try:
		dictionary=Dictionary().load("Topic/dic.tm")
		print "Dictionary loaded!"
	except IOError:
		print "Dictionary not found, building Dictionary..."
		dictionary=Dictionary(i for i in MyDictionary())
		#once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
		#dictionary.filter_tokens(once_ids)
		#dictionary.compactify() 
		print "\rDictionary Built!"
		print dictionary
		dictionary.save("Topic/dic.tm")
	return dictionary

def fetch_model():
	print "Fetching LDA Model..."
	try:
		lda = LdaModel.load('Topic/lda.tm')
		print "LDA Model loaded!..."
	except IOError:
		print "Model not found, building LDA..."
		corpus=MyCorpus()
		lda = LdaModel(corpus,num_topics=50,id2word=dictionary,update_every=1,chunksize=1000,passes=15)
		print "LDA Built!"
		lda.save('Topic/lda.tm')
	return lda

def get_suggestions(doc):
	global dictionary
	dictionary = fetch_dict()
	lda        = fetch_model()
	corpus     = MyCorpus()
	docs       = list(corpus)
	return lda[dictionary.doc2bow(doc)]

if __name__ == '__main__':

	print get_suggestions(['added','based','came'])

	"""
	dictionary = fetch_dict()
	lda        = fetch_model()
	corpus     = MyCorpus()
	docs       = list(corpus)
	for i in lda[dictionary.doc2bow(test)]:
		tmp=""
		for j in docs[i[0]]:
			tmp+=dictionary[j[0]]+" "
		print tmp+"\n"
	"""
