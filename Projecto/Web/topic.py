import cherrypy
from sqlite3 import connect
from operator import itemgetter
from dateutil import parser

class Topic(object):

	def __init__(self, ac):
		self.ac_terms = ac

	@cherrypy.expose
	def default(self, uid='1', tid='1', page='1'):
		if page < '1':
			raise cherrypy.HTTPRedirect("/topic/"+uid+"/1/1")
		elif page > '5':
			raise cherrypy.HTTPRedirect("/topic/"+uid+"/1/5")
		database = connect('../Database/database.db')
		for row in database.execute('SELECT tpc_name FROM topics where tpc_id = '+tid+';'):
			topic = str(row[0])
		return """
<head data-live-domain="jquery.com">
	<meta charset="utf-8">

	<title>News Feed - Topics</title>

	<link rel="stylesheet" href="http://jqueryui.com/jquery-wp-content/themes/jquery/css/base.css?v=1">
	<link rel="stylesheet" href="http://jqueryui.com/jquery-wp-content/themes/jqueryui.com/style.css">

	<link rel="stylesheet" href="http://jquery.com/jquery-wp-content/themes/jquery/css/base.css?v=1">
	<link rel="stylesheet" href="http://jquery.com/jquery-wp-content/themes/jquery.com/style.css">

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

	<script src="http://jquery.com/jquery-wp-content/themes/jquery/js/modernizr.custom.2.6.2.min.js"></script>

	<script src="http://jquery.com/jquery-wp-content/themes/jquery/js/plugins.js"></script>
	<script src="http://jquery.com/jquery-wp-content/themes/jquery/js/main.js"></script>

	<script src="//use.typekit.net/wde1aof.js"></script>
	<script>try{Typekit.load();}catch(e){}</script>

	<link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
	<script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
	<script>
	$(function() {
		var availableTags = """+str(self.ac_terms)+""";
		function split( val ) {return val.split( / \s*/ );}
		function extractLast( term ) {return split( term ).pop();}
		$( "#searchbar" )
			.bind( "keydown", function( event ) {
				if ( event.keyCode === $.ui.keyCode.TAB && $( this ).data( "ui-autocomplete" ).menu.active ) {event.preventDefault();}
			})
			.autocomplete({
				//autoFocus: true,
				//delay: 500,
				//minLength: 3,
				//source: function( request, response ) {
				//	response( $.ui.autocomplete.filter(availableTags, extractLast( request.term ) ) );
				//},
				source: function( request, response ) {
					var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( extractLast( request.term ) ), "i" );
					//response( $.grep( availableTags, function( item ){return matcher.test( item );}) );
					var results = $.grep( availableTags, function( item ){return matcher.test( item );});
					response(results.slice(0, 5));
				},
				search: function() {
					var term = extractLast( this.value );
					if ( term.length < 3 ) {return false;}
				},
				focus: function() {return false;},
				select: function( event, ui ) {
					var terms = split( this.value );
					terms.pop();
					terms.push( ui.item.value );
					terms.push( "" );
					this.value = terms.join( " " );
					return false;
				}
			});
	});
	</script>

	<style media="screen" type="text/css">
		.ui-menu, .ui-menu-item a{
		color: #606060;
		border-radius: 10px;
		font-size:12px;
		width:333px;
	}
	</style>

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
				</ul>
			</div>

			<form method="post" class="searchform" action="/search/"""+str(uid)+"""/1">
				<button type="submit" class="icon-search"><span class="visuallyhidden">search</span></button>
					<label>
					<span class="visuallyhidden">Search</span>
					<div class="ui-widget">
					<input id="searchbar" type="text" name="search" value="" placeholder="Search">
					</div>
				</label>
			</form>
		</nav>

		<div id="content-wrapper" class="clearfix row">

			<div class="content-right twelve columns">
				<div id="content" style="width:75%">

					""" + self.get_topic_docs(uid, tid, page) + """


					<div class="pagination">
						""" + self.topic_pagination(uid, tid, page) + """
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

	def topic_pagination(self, uid='1', tid='1', page='1'):

		string = ''
		for i in range(1,self.num_pages+1):
			if page == str(i):
				string += "<span class='page-numbers current'><b style=\"color:#909090;\">"+str(i)+"</b></span>\n"
			else:
				string += "<a class='page-numbers' href='/topic/"+uid+"/"+tid+"/"+str(i)+"'\"><b>"+str(i)+"</b></a>\n"

		return string

	def get_topic_docs(self, uid='1', tid='1', page='1'):
		uid = int(uid)
		page = int(page)

		database = connect('../Database/database.db')

		docids = []
		for row in database.execute('SELECT doc_id FROM documents,tpc_doc where doc_id = tpd_document'+\
			' and tpd_topic = '+tid+';'):
			docids.append(row[0])
		docs = [{'urating':2,'view':0,'preftv':0,'preftr':2.5} for i in range(len(docids))]

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
			doc['score'] = 3.5*(1^doc['view']) + 2*doc['rating'] + 1.5*doc['urating'] + \
						   2*doc['views'] + doc['preftv']*0.5 + doc['preftr']*0.5

		docs.sort(key=itemgetter('score'), reverse = True)

		self.num_pages = min(len(docs)/10 + min(len(docs)%10,1),5)

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
