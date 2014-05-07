import cherrypy

class Topic(object):

	@cherrypy.expose
	def default(self, uid='1', tid='1', page='1'):
		if page < '1':
			raise cherrypy.HTTPRedirect("/topic/"+uid+"/1/1")
		elif page > '5':
			raise cherrypy.HTTPRedirect("/topic/"+uid+"/1/5")
		return """
<head data-live-domain="jquery.com">
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

	<title>News Feed - Topics</title>

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
					<li class="menu-item"><a href="/home">Home</a></li>
					<li class="menu-item"><a href="/recommend">Recommended</a></li>
				</ul>
			</div>

			<form method="get" class="searchform" action="https://jqueryui.com/">
				<button type="submit" class="icon-search"><span class="visuallyhidden">search</span></button>
					<label>
					<span class="visuallyhidden">Search jQuery UI</span>
					<input type="text" name="s" value="" placeholder="Search">
				</label>
			</form>
		</nav>

		<div id="content-wrapper" class="clearfix row">

			<div class="content-right twelve columns">
				<div id="content">
					""" + self.get_topic_docs(uid, tid, page) + """


					<div class="pagination">
						""" + self.topic_pagination(uid, tid, page) + """
					</div>

				</div>

				<div id="sidebar" class="widget-area" role="complementary" width=10px>
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
						<li><a href="/topic/"""+uid+"""/13">Sports</a></li>
						<li><a href="/topic/"""+uid+"""/9">History</a></li>
						<li><a href="/topic/"""+uid+"""/14">Capital</a></li>
						<li><a href="/topic/"""+uid+"""/12">Nature</a></li>
						<li><a href="/topic/"""+uid+"""/10">Consumer</a></li>
						<li><a href="/topic/"""+uid+"""/11">Culture</a></li>
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

	def topic_pagination(self, uid='1', tid='1', page='1'):

		string = ''
		if page == '1': string += "<span class='page-numbers current'><b style=\"color:#909090;\">1</b></span>\n"
		else: string += "<a class='page-numbers' href='/topic/"+uid+"/"+tid+"/1'\"><b>1</b></a>\n"
		if page == '2': string += "<span class='page-numbers current'><b style=\"color:#909090;\">2</b></span>\n"
		else: string += "<a class='page-numbers' href='/topic/"+uid+"/"+tid+"/2'\"><b>2</b></a>\n"
		if page == '3': string += "<span class='page-numbers current'><b style=\"color:#909090;\">3</b></span>\n"
		else: string += "<a class='page-numbers' href='/topic/"+uid+"/"+tid+"/3'\"><b>3</b></a>\n"
		if page == '4': string += "<span class='page-numbers current'><b style=\"color:#909090;\">4</b></span>\n"
		else: string += "<a class='page-numbers' href='/topic/"+uid+"/"+tid+"/4'\"><b>4</b></a>\n"
		if page == '5': string += "<span class='page-numbers current'><b style=\"color:#909090;\">5</b></span>\n"
		else: string += "<a class='page-numbers' href='/topic/"+uid+"/"+tid+"/5'\"><b>5</b></a>\n"

		return string

	def get_topic_docs(self, uid='1', tid='1', page='1'):
		uid = int(uid)
		page = int(page)

		from sqlite3 import connect
		from operator import itemgetter
		from dateutil import parser

		database = connect('../Database/database.db')

		docids = []
		for row in database.execute('SELECT doc_id FROM documents,tpc_doc where doc_id = tpd_document'+\
			' and tpd_topic = '+tid+';'):
			docids.append(row[0])
		docs = [{'urating':2.5,'view':0,'preftv':0,'preftr':2.5} for i in range(len(docids))]

		max_views = 0

		for n,did in enumerate(docids):
			for row in database.execute('SELECT doc_id,doc_rating,doc_nviews from documents'+\
				' where doc_id = '+str(did)+' ;'):
				docs[n]['id'] = row[0]
				docs[n]['rating'] = row[1]/5.0
				docs[n]['views'] = row[2]
				if row[2] > max_views: max_views = row[2]
			for row in database.execute('SELECT hst_rating,hst_view from historics'+\
				' where hst_document = '+str(did)+' and hst_user = '+str(uid)+';'):
				docs[n]['urating'] = row[0]/5.0
				docs[n]['view'] = row[1]
			for row in database.execute('SELECT tpp_nviews/usr_nviews, tpp_rating from users,'+\
			    'tpc_preferences where tpp_user = '+str(uid)+' and usr_id = '+str(uid)+';'):
				docs[n]['preftv'] = row[0]
				docs[n]['preftr'] = row[1]/5.0

		if max_views != 0:
			for doc in docs:
				doc['views'] /= 1.0 * max_views

		for doc in docs:
			doc['score'] = 0.35*doc['view'] + 1.75*doc['rating'] + 1.25*doc['urating'] + \
			               2.5*doc['views'] + doc['preftv']*0.5 + doc['preftr']*0.5

		docs.sort(key=itemgetter('score'), reverse = True)
		docs = docs[(page-1)*10:page*10]
		strings=[]
		for n,did in enumerate([doc['id'] for doc in docs]):
			for row in database.execute('SELECT doc_datetime,doc_thumbnail,doc_title,doc_description'+\
			' from documents where doc_id = '+str(did)+';'):
				if docs[n]['view'] == 1: opacity = '0.6'; color = '#909090'
				else:                    opacity = '1'; color = '#303030'
				strings.append('<table><tr style="border-bottom: 1px solid #666;"><td width="170px";'+\
					' vertical-align=middle;><img src="'+str(row[1])+'" style="opacity:'+opacity+';""></td>')
				strings[-1] += '<td><h2><a href="/document/'+str(uid)+'/'+str(did)+\
					'" style="color:'+color+';">' + str(row[2]) + '</a></h2>\n'
				strings[-1] += '<p style="color:#606060; font-size:15"><span style="color:#A0A0A0">'
				strings[-1] += parser.parse(str(row[0])).strftime('%d/%m/%Y')+'</span>'
				strings[-1] += ' - ' + str(row[3]) + '</p></td></tr></table>\n'
				#strings[-1] += '\n<hr class="dots"/>\n'

		return ''.join(strings)
