from gensim.models.ldamodel import LdaModel
from gensim.models import TfidfModel

from gensim import similarities

from gensim.corpora import Dictionary

from cPickle import load
from pprint import pprint

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
			lda = LdaModel(corpus,num_topics=50,id2word=dictionary,update_every=1,chunksize=1000,passes=15)
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

if __name__ == '__main__':

	test=['list', 'school', 'ofsted', 'sent', 'inspect', 'alleged', 'plot', 'muslim', 'hard-liners', 'seize', 'control', 'governing', 'body', 'published', 'birmingham', 'city', 'council', 'carrying', 'inquiry', 'allegation', 'made', 'public', 'list', '18', 'school', 'ofsted', 'inspected', 'council', 'leader', 'sir', 'albert', 'bore', 'ofsted', 'publish', 'report', 'first', 'second', 'week', 'may', 'council', 'yet', 'seen', 'draft', 'version', 'report', 'sir', 'albert', 'went', 'criticise', 'apparent', 'leaking', 'education', 'funding', 'agency', 'report', 'three', 'city', 'academy', 'national', 'newspaper', 'weekend', 'government', 'cabinet', 'office', 'investigating', 'source', 'trojan', 'horse', 'allegation', 'first', 'came', 'light', 'earlier', 'year', 'contained', 'anonymous', 'unsigned', 'letter', '25', 'school', 'investigated', 'claim', 'male', 'female', 'pupil', 'segregated', 'sex', 'education', 'banned', 'one', 'case', 'al', 'qaida-linked', 'muslim', 'cleric', 'anwar', 'al-awlaki', 'praised', 'assembly', 'preacher', 'killed', 'us', 'drone', 'strike', 'yemen', '2011', 'saturday', 'daily', 'telegraph', 'reported', 'six', 'school', 'implicated', 'allegation', 'faced', 'placed', 'special', 'measure', 'sir', 'albert', 'important', 'sensitive', 'information', 'leaked', 'time', 'wholly', 'reprehensible', 'completely', 'unacceptable', 'one', 'school','word']

	test2=['emma', 'brant', 'newsbeat', 'reporter', 'april', 'last', 'updated', 'hollywood', 'director', 'bryan', 'singer', 'spoken', 'sex', 'abuse', 'accusation', 'made', 'announced', 'miss', 'forthcoming', 'press', 'event', 'new', 'x-men', 'film', 'statement', 'branded', 'claim', 'outrageous', 'vicious', 'false', 'statement', 'came', 'aspiring', 'actor', 'michael', 'egan', 'filed', 'legal', 'case', 'april', 'claiming', 'sexually', 'abused', 'singer', 'accusation', 'date', 'back', 'hawaii', 'california', 'singer', 'statement', 'confirmed', 'withdrawing', 'upcoming', 'medium', 'event', 'latest', 'film', 'want', 'fictitious', 'claim', 'divert', 'attention', 'x-men', 'day', 'future', 'past', 'fantastic', 'film', 'labour', 'love', 'greatest', 'experience', 'career', 'respect', 'extraordinary', 'contribution', 'incredibly', 'talented', 'actor', 'crew', 'involved', 'decided', 'participate', 'upcoming', 'medium', 'event', 'film', 'however', 'promise', 'situation', 'fact', 'show', 'sick', 'twisted', 'shake', 'want', 'thank', 'fan','friend', 'family', 'amazing', 'overwhelming', 'support', 'michael', 'egan', 'claim', 'subjected', 'drug', 'alcohol', 'threat', 'part', 'wider', 'group', 'adult', 'male', 'similarly', 'positioned', 'entertainment', 'industry', 'singer', 'lawyer', 'marty', 'singer', 'director', 'hawaii', 'egan', 'claim', 'abused', 'earlier', 'week', 'singer', 'also', 'accuser', 'lawyer', 'jeff', 'herman', 'behaved', 'reckless', 'outrageous', 'conduct', 'case', 'egan', 'also', 'sued', 'entertainment', 'industry', 'figure', 'former', 'television', 'executive', 'theatre', 'producer', 'claim', 'lured', 'sex', 'ring', 'promise', 'audition', 'acting', 'modelling', 'put', 'payroll', 'actor', 'forced', 'sex', 'men', 'party', 'entertainment', 'industry', 'hollywood', 'us', 'medium', 'decided', 'reveal', 'identity', 'michael', 'egan', 'speaking', 'publicly', 'claim', 'usually', 'name', 'victim', 'sex', 'abuse', 'published', 'america', 'x-men', 'day', 'future', 'past', 'set', 'release', 'may', 'follow', 'bbcnewsbeat', 'twitter']
	print get_similar(test2)


	
