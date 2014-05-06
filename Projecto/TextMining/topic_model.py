from gensim.models.ldamodel import LdaModel
from gensim.models import TfidfModel

from gensim import similarities

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
	#for c in corpus:
	#	print dictionary.doc2bow(doc)

	vec_bow = dictionary.doc2bow(doc)
	vec_lda = lda[vec_bow] # convert the query to LSI 
	print(vec_lda)

	corp=[i for i in corpus]

	pprint( sorted(lda.print_topics(50),reverse=True))

	index = similarities.MatrixSimilarity(lda[corp])

	sims = index[vec_lda]


	return sorted(enumerate(sims),key=lambda item: -item[1])[:10]
	#return lda[dictionary.doc2bow(doc)]

if __name__ == '__main__':

	test=['list', 'school', 'ofsted', 'sent', 'inspect', 'alleged', 'plot', 'muslim', 'hard-liners', 'seize', 'control', 'governing', 'body', 'published', 'birmingham', 'city', 'council', 'carrying', 'inquiry', 'allegation', 'made', 'public', 'list', '18', 'school', 'ofsted', 'inspected', 'council', 'leader', 'sir', 'albert', 'bore', 'ofsted', 'publish', 'report', 'first', 'second', 'week', 'may', 'council', 'yet', 'seen', 'draft', 'version', 'report', 'sir', 'albert', 'went', 'criticise', 'apparent', 'leaking', 'education', 'funding', 'agency', 'report', 'three', 'city', 'academy', 'national', 'newspaper', 'weekend', 'government', 'cabinet', 'office', 'investigating', 'source', 'trojan', 'horse', 'allegation', 'first', 'came', 'light', 'earlier', 'year', 'contained', 'anonymous', 'unsigned', 'letter', '25', 'school', 'investigated', 'claim', 'male', 'female', 'pupil', 'segregated', 'sex', 'education', 'banned', 'one', 'case', 'al', 'qaida-linked', 'muslim', 'cleric', 'anwar', 'al-awlaki', 'praised', 'assembly', 'preacher', 'killed', 'us', 'drone', 'strike', 'yemen', '2011', 'saturday', 'daily', 'telegraph', 'reported', 'six', 'school', 'implicated', 'allegation', 'faced', 'placed', 'special', 'measure', 'sir', 'albert', 'important', 'sensitive', 'information', 'leaked', 'time', 'wholly', 'reprehensible', 'completely', 'unacceptable', 'one', 'school','word']

	print get_suggestions(test)


	
