from gensim.models.ldamodel import LdaModel
from gensim.models import TfidfModel

from gensim.corpora.dictionary import Dictionary

from cPickle import load
from pprint import pprint

class MyCorpus(object):
	def __iter__(self):
		f=open("terms.dat","rb")
		total=load(f)
		for i in range(total):
			yield dictionary.doc2bow(load(f))
		
if __name__ == '__main__':
	
	"""
	corpus=MyCorpus()
	dictionary=Dictionary(i for i in corpus)

	#once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
	#dictionary.filter_tokens(once_ids) # remove stop words and words that appear only once
	#dictionary.compactify() # remove gaps in id sequence after words that were removed

	dictionary.save("dictionary.dict")
	"""
	dictionary=Dictionary().load("dictionary.dict")
	
	corpus=MyCorpus()

	lda = LdaModel(corpus,num_topics=50,id2word=dictionary,update_every=1,chunksize=1000,passes=15)
	lda.save('lda')
	pprint(sorted(lda.print_topics(50),reverse=True))
	

