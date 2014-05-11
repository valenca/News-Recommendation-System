import cherrypy
from topic import Topic
from document import Document
from tag import Tag
from recommend import Recommend
from search import Search
from advsearch import AdvSearch
from sqlite3 import connect
from operator import itemgetter
from dateutil import parser

class Home(object):

	@cherrypy.expose
	def index(self, uid='1'):
		raise cherrypy.HTTPRedirect("/home/1")

	@cherrypy.expose
	def home(self, uid='1',page='1'):
		if page < '1':
			raise cherrypy.HTTPRedirect("/home/"+uid+"/1")
		elif page > '5':
			raise cherrypy.HTTPRedirect("/home/"+uid+"/5")
		return """
<head data-live-domain="jquery.com">
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<link rel="stylesheet" type="text/css" href="styles.css">

	<title>News Feed - Home</title>

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
					<input type="text" name="search" value="" placeholder="Search">
				</label>
			</form>
		</nav>

		<div id="content-wrapper" class="clearfix row">

			<div class="content-right twelve columns">
				<div id="content" style="width:75%">
					""" + self.get_home_docs(uid, page) + """


					<div class="pagination">
						""" + self.home_pagination(uid, page) + """
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

	def home_pagination(self, uid='1', page='1'):

		string = ''
		if page == '1': string += "<span class='page-numbers current'><b style=\"color:#909090;\">1</b></span>\n"
		else: string += "<a class='page-numbers' href='/home/"+uid+"/1'\"><b>1</b></a>\n"
		if page == '2': string += "<span class='page-numbers current'><b style=\"color:#909090;\">2</b></span>\n"
		else: string += "<a class='page-numbers' href='/home/"+uid+"/2'\"><b>2</b></a>\n"
		if page == '3': string += "<span class='page-numbers current'><b style=\"color:#909090;\">3</b></span>\n"
		else: string += "<a class='page-numbers' href='/home/"+uid+"/3'\"><b>3</b></a>\n"
		if page == '4': string += "<span class='page-numbers current'><b style=\"color:#909090;\">4</b></span>\n"
		else: string += "<a class='page-numbers' href='/home/"+uid+"/4'\"><b>4</b></a>\n"
		if page == '5': string += "<span class='page-numbers current'><b style=\"color:#909090;\">5</b></span>\n"
		else: string += "<a class='page-numbers' href='/home/"+uid+"/5'\"><b>5</b></a>\n"

		return string

	def get_home_docs(self, uid='1', page='1'):
		uid = int(uid)
		page = int(page)

		database = connect('../Database/database.db')

		docids = []
		for row in database.execute('SELECT doc_id FROM documents;'):
			docids.append(row[0])
		docs = [{'urating':2,'view':0} for i in range(len(docids))]

		max_views = 0

		for n,did in enumerate(docids):
			for row in database.execute('SELECT doc_id,doc_rating,doc_nviews from documents'+\
				' where doc_id = '+str(did)+';'):
				docs[n]['id'] = row[0]
				docs[n]['rating'] = row[1]/5.0
				docs[n]['views'] = row[2]
				if row[2] > max_views: max_views = row[2]
			for row in database.execute('SELECT hst_rating from historics'+\
				' where hst_document = '+str(did)+' and hst_user = '+str(uid)+';'):
				docs[n]['urating'] = row[0]/5.0
				docs[n]['view'] = 1
			docs[n]['topics'] = []
			for row in database.execute('SELECT tpc_id from topics,tpc_doc'+\
				' where tpc_id = tpd_topic and tpd_document = '+str(did)+';'):
				docs[n]['topics'].append(row[0])
			docs[n]['preftv'] = 0; docs[n]['preftr'] = 0
			for t in docs[n]['topics']:
				for row in database.execute('SELECT tpp_nviews/usr_nviews, tpp_rating from users,'+\
					'tpc_preferences where tpp_user = '+str(uid)+' and usr_id = '+str(uid)+' and tpp_topic = '+str(t)+';'):
					docs[n]['preftv'] += row[0] if row[0] is not None else 0
					docs[n]['preftr'] += row[1]/5.0
			docs[n]['preftr'] /= float(len(docs[n]['topics']))
			docs[n]['preftv'] /= float(len(docs[n]['topics']))

		if max_views != 0:
			for doc in docs:
				doc['views'] /= 1.0 * max_views

		for doc in docs:
			doc['score'] = 0.35*doc['view'] + 2*doc['rating'] + 1.5*doc['urating'] + \
						   2*doc['views'] + doc['preftv']*0.5 + doc['preftr']*0.5

		docs.sort(key=itemgetter('score'), reverse = True)
		docs = docs[(page-1)*10:page*10]
		strings=[]
		for n,did in enumerate([doc['id'] for doc in docs]):
			for row in database.execute('SELECT doc_datetime,doc_thumbnail,doc_title,doc_description'+\
			' from documents where doc_id = '+str(did)+';'):
				if docs[n]['view'] == 1: opacity = '0.6'; color = '#909090'
				else:					opacity = '1'; color = '#303030'
				strings.append('<table><tr style="border-bottom: 1px solid #666;"><td width="170px";>'+\
					'<img src="'+str(row[1])+'" style="opacity:'+opacity+';""></td>')
				strings[-1] += '<td><h2><a href="/document/'+str(uid)+'/'+str(did)+\
					'" style="color:'+color+';">' + str(row[2]) + '</a></h2>\n'
				strings[-1] += '<p style="color:#606060; font-size:15"><span style="color:#A0A0A0">'
				strings[-1] += parser.parse(str(row[0])).strftime('%d/%m/%Y')+'</span>'
				if str(row[3]) != '':
					strings[-1] += ' - ' + str(row[3])
				strings[-1] += '</p></td></tr></table>\n'
				#strings[-1] += '\n<hr class="dots"/>\n'

		return ''.join(strings)

if __name__ == '__main__':
	root = Home()
	root.topic = Topic()
	root.document = Document()
	root.tag = Tag()
	root.recommend = Recommend()
	root.search = Search()
	root.advsearch = AdvSearch()
	cherrypy.server.socket_host = '192.168.1.95'
	cherrypy.engine.start()
	cherrypy.quickstart(root)
