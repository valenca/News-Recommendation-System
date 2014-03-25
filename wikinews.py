import nltk, string, os.path
from sklearn import cross_validation
from pickle import dump, load

class Document():

	def __init__(self):
		self.info = []
		self.topic = ''
		self.title = ''
		self.date = ''
		self.sentences = []
		self.tokens = []
		self.entities = []
		self.tags_t = []
		self.tags = []
		self.stems = []

def parser(documents):
	line = '.'
	with open('Dataset_Wikinews.txt') as f:
		while True:
			line_t = line
			line = f.readline()[:-1]
			if line_t == line == '': break
			documents.append(Document())
			documents[len(documents)-1].topic = line
			documents[len(documents)-1].title = f.readline()[:-1]
			documents[len(documents)-1].date = f.readline()[:-1]
			while True:
				line = f.readline()[:-1]
				if line == '': break
				documents[len(documents)-1].info.append(line)

def sentencer(documents):
	# Divide paragraphs of a document into sentences
	for i in documents: i.sentences.append(i.topic+'.')
	for i in documents: i.sentences.append(i.title+'.')
	for i in documents: i.sentences.append(i.date+'.')
	for i in documents: [[i.sentences.append(k) for k in nltk.tokenize.sent_tokenize(j)] for j in i.info]

def tokenizer(documents):
	# Divide sentences of a document into tokens
	for i in documents: [[i.tokens.append(k) for k in nltk.tokenize.word_tokenize(j)] for j in i.sentences]
	
def tagger(documents):
	# Initial PosTag to get entities from a document
	for i in documents: i.tags_t = nltk.tag.pos_tag(i.tokens)

	if False:
		# Get entities from inital postag
		for i in documents:
			entities = [j for j in nltk.chunk.ne_chunk(i.tags_t, binary=False) if hasattr(j, 'node')]
			entities = [[j.node,' '.join([k[0] for k in j.leaves()])] for j in entities]
			# Remove duplicates
			entities = [list(k) for k in list(set([tuple(j) for j in entities]))]
			# Remove included
			for j in range(len(entities)):
				temp = 0
				for k in range(len(entities)):
					if j != k and entities[j][0] == entities[k][0] and entities[j][1] in entities[k][1]:
						temp = 1; break
				if temp == 0: i.entities.append(entities[j])

	# PosTag to lowercase tokens
	for i in documents:
		i.tags_t = nltk.tag.pos_tag(map(string.lower, i.tokens))

	# Remove punctuation tags and stopwords
	punctuation = list(string.punctuation)+['``','\'\'','...']
	for i in documents:
		i.tags_t = [j for j in i.tags_t if j[0] not in punctuation and j[1] not in punctuation]
		i.tags_t = [j for j in i.tags_t if j[0] not in nltk.corpus.stopwords.words('english')]

	# Remove any other tags
	remove_list = ['POS','PRP','PRP$','IN','TO','CC','DT']
	for i in documents:
		i.tags = [j[0] for j in i.tags_t if j[1] not in remove_list]
	
	# Replace words
	replace_list = [["\'s",'is'],["\'re",'are'],["\'m",'am'],["\'ll",'will'],["\'ve",'have'],["n\'t",'not'],
				   ["\'97",'1997']]
	for i in documents:
		for j in range(len(i.tags)):
			for k in replace_list:
				if i.tags[j] == k[0]:
					i.tags[j] = k[1]
					break

def stemmer(documents):
	# Lemmatize tags
	stemmer = nltk.stem.wordnet.WordNetLemmatizer()
	for i in documents: i.stems = [stemmer.lemmatize(j) for j in i.tags]

def get_terms(documents):
	# Get all terms
	terms = []
	for i in documents: terms.extend(i.stems)
	return list(set(terms))

def get_occurrences(documents, terms):
	# Get occurrences
	occurrences = []
	for i in documents:
		occurrences.append([i.stems.count(j) for j in terms])
	return occurrences

def get_existences(occurrences):
	# Get existences
	#existences = [[min(j,1) for j in i] for i in occurrences]
	return [list(map(lambda (x):min(x,1),i)) for i in occurrences]

def get_tp_data(documents, terms, existences):
	# Get tuples with correspondences
	tp_features = []
	for i in range(len(documents)):
		tp_features.append((dict(zip(terms,existences[i])),documents[i].topic))
	return tp_features

def cv_tester(tp_features):
	cv = cross_validation.KFold(len(tp_features), n_folds=len(tp_features)/5, shuffle=True)

	for train_set, test_set in cv:
		classifier = nltk.DecisionTreeClassifier.train([tp_features[i] for i in train_set])
		results = classifier.batch_classify([tp_features[i][0] for i in test_set])
		print 'Results: ' + str([tp_features[i][1] for i in test_set]) + " - " + str(results)
		#for pdist in classifier.batch_prob_classify([tp_features[i][0] for i in test_set]):
		#	print '%.4f %.4f' % (pdist.prob('Sports'), pdist.prob('Economy'))
		print 'Accuracy: ', nltk.classify.util.accuracy(classifier, [tp_features[i] for i in test_set])
		#print classifier.show_most_informative_features()

if __name__ == '__main__':

	if not os.path.isfile('features.dat'):

		documents = []

		## Feature Extraction ##
		parser(documents)
		sentencer(documents)
		tokenizer(documents)
		tagger(documents)
		stemmer(documents)
		########################

		## Text Modeling ##
		terms = get_terms(documents)
		occurrences = get_occurrences(documents, terms)
		existences = get_existences(occurrences)
		tp_features = get_tp_data(documents, terms, existences)
		with open('features.dat','wb') as f:
			dump(tp_features, f)
		###################
	else:
		with open('features.dat','rb') as f:
			tp_features = load(f)

	## Cross-Validation Test ##
	cv_tester(tp_features)


'''def csv(documents):
	# Remove commas
	for i in documents: i.stems = [j.replace(',','') for j in i.stems]

	# Get all terms
	terms = []
	for i in documents: terms.extend(i.stems)
	terms = list(set(terms))

	# Write CSV file
	with open("database.csv", "w") as f:
		f.write(','.join(terms) + "\n")
		for i in documents:
			f.write(','.join(list(map(str, [i.stems.count(j) for j in terms]))) + "\n")'''
