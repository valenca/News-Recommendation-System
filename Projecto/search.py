import os.path
from whoosh.fields import Schema, NUMERIC, DATETIME, TEXT, STORED
from whoosh.index import create_in, open_dir
from whoosh.analysis import StemmingAnalyzer

ana = StemmingAnalyzer(stoplist=None)

if not os.path.isdir("indexd"):
	os.mkdir("indexd")
	schema = Schema(id=NUMERIC(stored=True,unique=True),
					datetime=DATETIME,
					title=TEXT(field_boost=20),
					description=TEXT(field_boost=10),
					text=TEXT(field_boost=6),
					topics=TEXT(field_boost=3),
					text2=TEXT(stored=True,field_boost=0,analyzer=ana))
	create_in('indexd', schema)

index = open_dir('indexd')
writer = index.writer()

from dateutil import parser
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.collectors import TimeLimitCollector, TimeLimit
datetime1 = parser.parse('2014-01-20 08:14:17')
writer.add_document(title=['one','two','three'],text=['four','five','six'],
	datetime=datetime1,text2=u"four five six eight")
datetime2 = parser.parse('2013-02-21 08:14:16')
writer.add_document(title=['four','five','six'],text=['seven','eight','business'],
	datetime=datetime2,text2=u"seven eight of's businesses")
writer.commit()
from whoosh import scoring
with index.searcher(weighting=scoring.TF_IDF()) as searcher:
	from whoosh.qparser import MultifieldParser
	parser = MultifieldParser(['title','text','datetime','text2'],index.schema)
	parser.add_plugin(DateParserPlugin())
	myquery = parser.parse('fours OR ofs OR business OR sev')

	c = searcher.collector()
	tlc = TimeLimitCollector(c, timelimit=0.5)
	try:
		searcher.search_with_collector(myquery, tlc)
	except TimeLimit:
		print("Search took too long, aborting!")
	
	#results = tlc.results()
	results = searcher.search(myquery)

	for i in range(len(results[:])):
		print results[i],
		print results.score(i)
		print(results[i].highlights("text2"))
