import cherrypy
from sqlite3 import connect
from operator import itemgetter
from dateutil import parser

from whoosh.index import open_dir
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh import scoring
from whoosh.qparser import MultifieldParser

class Search(object):
	
	def __init__(self):
		self.index = open_dir('../TextMining/Index')

	@cherrypy.expose()
	def default(self, uid='1', typ='1', page='1', search=''):
		if page < '1':
			raise cherrypy.HTTPRedirect("/search/"+uid+"/"+typ+"/1/"+search)
		elif page > '5':
			raise cherrypy.HTTPRedirect("/search/"+uid+"/"+typ+"/5/"+search)
		return """
<head data-live-domain="jquery.com">
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

	<title>News Feed - Search</title>

	<meta name="author" content="jQuery Foundation - jquery.org">
	<meta name="description" content="jQuery: The Write Less, Do More, JavaScript Library">

	<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
	<meta http-equiv="Pragma" content="no-cache" />
	<meta http-equiv="Expires" content="0" />

	<meta name="viewport" content="width=device-width">

	<link rel="stylesheet" href="http://jqueryui.com/jquery-wp-content/themes/jquery/css/base.css?v=1">
	<link rel="stylesheet" href="http://jqueryui.com/jquery-wp-content/themes/jqueryui.com/style.css">

	<link rel="stylesheet" href="http://jquery.com/jquery-wp-content/themes/jquery/css/base.css?v=1">
	<link rel="stylesheet" href="http://jquery.com/jquery-wp-content/themes/jquery.com/style.css">
	<link rel="pingback" href="http://jquery.com/xmlrpc.php" />
	<!--[if lt IE 7]><link rel="stylesheet" href="css/font-awesome-ie7.min.css"><![endif]-->

	<script src="http://jquery.com/jquery-wp-content/themes/jquery/js/modernizr.custom.2.6.2.min.js"></script>

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
	<script>window.jQuery || document.write(unescape('%3Cscript src="http://jquery.com/jquery-wp-content/themes/jquery/js/jquery-1.9.1.min.js"%3E%3C/script%3E'))</script>

	<script src="http://jquery.com/jquery-wp-content/themes/jquery/js/plugins.js"></script>
	<script src="http://jquery.com/jquery-wp-content/themes/jquery/js/main.js"></script>

	<script src="//use.typekit.net/wde1aof.js"></script>
	<script>try{Typekit.load();}catch(e){}</script>

<script type='text/javascript' src='http://jquery.com/wp-includes/js/comment-reply.min.js?ver=3.8'></script>
<meta name="generator" content="WordPress 3.8" />

</head>
<body class="jquery home page page-id-5 page-template page-template-page-fullwidth-php page-slug-index single-author singular">

	<div id="container">
		<div id="logo-events" class="constrain clearfix">
			<h2> </h2>
		</div>

		<nav id="main" class="constrain clearfix">
			<div class="menu-top-container">
				<ul id="menu-top" class="menu">
					<li class="menu-item"><a href="/home/"""+str(uid)+"""">Home</a></li>
					<li class="menu-item"><a href="/recommend/"""+str(uid)+"""">Recommended</a></li>
					<li class="menu-item" style="float:right"><a href="/advsearch/"""+str(uid)+"""">Advanced Search</a></li>
				</ul>
			</div>

			<form method="post" class="searchform" action="/search/"""+str(uid)+"""/1">
				<button type="submit" class="icon-search"><span class="visuallyhidden">search</span></button>
					<label>
					<span class="visuallyhidden">Search</span>
					<input type="text" name="search" value=\""""+str(search)+"""\" placeholder="Search">
				</label>
			</form>
		</nav>

		<div id="content-wrapper" class="clearfix row">

			<div class="content-right twelve columns">
				<div id="content" style="width:75%">

					""" + self.get_search(uid,typ,page,search) + """

					<div class="pagination">
						""" + self.search_pagination(uid,typ,page,search) + """
					</div>

				</div>

				<div id="sidebar" class="widget-area" role="complementary" width=10px style="width:25%">
				<aside class="widget">
					<h3 class="widget-title">Topics</h3>
					<ul>
						<li><a href="/topic/"""+uid+"""/1">Business</a></li>
						<li><a href="/topic/"""+uid+"""/2">Politics</a></li>
						<li><a href="/topic/"""+uid+"""/3">Health</a></li>
						<li><a href="/topic/"""+uid+"""/4">Education</a></li>
						<li><a href="/topic/"""+uid+"""/5">Science & Environment</a></li>
						<li><a href="/topic/"""+uid+"""/6">Technology</a></li>
						<li><a href="/topic/"""+uid+"""/7">Entertainment & Arts</a></li>
						<li><a href="/topic/"""+uid+"""/8">Magazine</a></li>
						<li><a href="/topic/"""+uid+"""/9">History</a></li>
						<li><a href="/topic/"""+uid+"""/10">Consumer</a></li>
						<li><a href="/topic/"""+uid+"""/11">Arts & Culture</a></li>
						<li><a href="/topic/"""+uid+"""/12">Nature</a></li>
						<li><a href="/topic/"""+uid+"""/13">Sports</a></li>
						<li><a href="/topic/"""+uid+"""/14">Capital</a></li>
					</ul>
				</aside>
				</div>
			</div>
		</div>
	</div>

	<footer class="clearfix simple">
	</footer>



</body>
</html>"""

	def search_pagination(self, uid, typ, page, search):

		string = ''
		if page == '1': string += "<span class='page-numbers current'><b style=\"color:#909090;\">1</b></span>\n"
		else: string += "<a class='page-numbers' href='/search/"+uid+"/"+typ+"/1/"+search+"'\"><b>1</b></a>\n"
		if page == '2': string += "<span class='page-numbers current'><b style=\"color:#909090;\">2</b></span>\n"
		else: string += "<a class='page-numbers' href='/search/"+uid+"/"+typ+"/2/"+search+"'\"><b>2</b></a>\n"
		if page == '3': string += "<span class='page-numbers current'><b style=\"color:#909090;\">3</b></span>\n"
		else: string += "<a class='page-numbers' href='/search/"+uid+"/"+typ+"/3/"+search+"'\"><b>3</b></a>\n"
		if page == '4': string += "<span class='page-numbers current'><b style=\"color:#909090;\">4</b></span>\n"
		else: string += "<a class='page-numbers' href='/search/"+uid+"/"+typ+"/4/"+search+"'\"><b>4</b></a>\n"
		if page == '5': string += "<span class='page-numbers current'><b style=\"color:#909090;\">5</b></span>\n"
		else: string += "<a class='page-numbers' href='/search/"+uid+"/"+typ+"/5/"+search+"'\"><b>5</b></a>\n"

		return string

	def get_search(self, uid='1', typ='1', page='1', search=''):
		if typ == '1':
			return self.get_normal_search(uid, page, search)
		else:
			return self.get_adv_search(uid, page, search)

	def get_normal_search(self, uid, page, search):
		uid = int(uid)
		page = int(page)

		searcher = self.index.searcher(weighting=scoring.TF_IDF())
		parser = MultifieldParser(['datetime','title','s_title','description','s_description','text','s_text','topics'],self.index.schema)
		parser.add_plugin(DateParserPlugin())

		myquery = parser.parse(' OR '.join((search.split())))
		raw_results = searcher.search_page(myquery, page, pagelen=10)

		results = []
		max_score = 0
		for i in range(len(raw_results[:])):
			results.append({'urating':2.5,'view':0})
			results[-1]['id'] = int(raw_results[i]['id'])
			results[-1]['score'] = float(raw_results.score(i))
			if results[-1]['score'] > max_score: max_score = results[-1]['score']
			if raw_results[i].highlights("s_title") != '':
				results[-1]['s_title'] = raw_results[i].highlights("s_title")
			else: results[-1]['s_title'] = raw_results[i]["s_title"]
			if raw_results[i].highlights("s_description") != '':
				results[-1]['s_description'] = raw_results[i].highlights("s_description")
			else: results[-1]['s_description'] = raw_results[i]["s_description"]
			results[-1]['s_text'] = raw_results[i].highlights("s_text",top=5).replace('...',' ... ')
		for r in results: r['score'] /= float(max_score)

		database = connect('../Database/database.db')
		max_views = 0

		for n,did in enumerate([r['id'] for r in results]):
			for row in database.execute('SELECT doc_rating,doc_nviews,doc_thumbnail from documents'+\
				' where doc_id = '+str(did)+';'):
				results[n]['rating'] = row[0]/5.0
				results[n]['views'] = row[1]
				results[n]['thumbnail'] = str(row[2])
				if row[1] > max_views: max_views = row[1]
			for row in database.execute('SELECT hst_rating from historics'+\
				' where hst_document = '+str(did)+' and hst_user = '+str(uid)+';'):
				results[n]['urating'] = row[0]/5.0
				results[n]['view'] = 1
			results[n]['topics'] = []
			for row in database.execute('SELECT tpc_id from topics,tpc_doc'+\
				' where tpc_id = tpd_topic and tpd_document = '+str(did)+';'):
				results[n]['topics'].append(row[0])
			results[n]['preftv'] = 0; results[n]['preftr'] = 0
			for t in results[n]['topics']:
				for row in database.execute('SELECT tpp_nviews/usr_nviews, tpp_rating from users,'+\
					'tpc_preferences where tpp_user = '+str(uid)+' and usr_id = '+str(uid)+' and tpp_topic = '+str(t)+';'):
					results[n]['preftv'] += row[0] if row[0] is not None else 0
					results[n]['preftr'] += row[1]/5.0
			results[n]['preftr'] /= float(len(results[n]['topics']))
			results[n]['preftv'] /= float(len(results[n]['topics']))

		if max_views != 0:
			for r in results:
				r['views'] /= 1.0 * max_views

		for r in results:
			r['score'] = 6*r['score'] + 1*r['rating'] + 0.75*r['urating'] + \
						   1.5*r['views'] + r['preftv']*0.375 + r['preftr']*0.375

		results.sort(key=itemgetter('score'), reverse = True)
		string = ''
		for r in results:
			string += '<table><tr style="border-bottom: 1px solid #666;"><td width="170px";>\n'
			string += '<img src="'+r['thumbnail']+'";""></td>'
			string += '<td><a href="/document/'+str(uid)+'/'+str(r['id'])+'" style="color:#505050;:hover{text-decoration:none;}">'
			string += '<h2 style="color:#808080;margin-bottom:5;">'+r['s_title']+'</h2></a>'
			string += '<h4 style="color:#808080;margin-bottom:5;">'+r['s_description']+'</h4>'
			string += '<p style="color:#808080;margin-bottom:5; font-size:15">'+r['s_text']+'</p>'
			string += '</td></tr></table>\n'

		return string

	def get_adv_search(self, uid, search):
		pass
