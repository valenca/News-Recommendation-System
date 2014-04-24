import os.path
from whoosh.fields import Schema, NUMERIC, DATETIME, TEXT, STORED
from whoosh.index import create_in, open_dir

if not os.path.isdir("indexd"):
	os.mkdir("indexd")
	schema = Schema(id=NUMERIC,
					datetime=DATETIME(stored=True),
					title=TEXT(stored=True,field_boost=20),
					description=TEXT(stored=True,field_boost=10),
					text=TEXT(stored=True,field_boost=6),
					topic=TEXT(field_boost=3),
					text2=TEXT(stored=True,field_boost=0))
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
writer.add_document(title=['four','five','six'],text=['seven','eight','nine'],
	datetime=datetime2,text2=u"seven eight nine")
writer.commit()
from whoosh import scoring
with index.searcher(weighting=scoring.TF_IDF()) as searcher:
	from whoosh.qparser import MultifieldParser
	parser = MultifieldParser(['title','text','datetime','text2'],index.schema)
	#parser.add_plugin(DateParserPlugin())
	myquery = parser.parse('one two')

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
