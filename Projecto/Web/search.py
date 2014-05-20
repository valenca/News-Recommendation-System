import cherrypy
from sqlite3 import connect
from operator import itemgetter
from dateutil import parser
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

from whoosh.index import open_dir
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh import scoring
from whoosh.qparser import MultifieldParser

class Search(object):
	
	def __init__(self, ac):
		self.index = open_dir('../TextMining/Index')
		self.ac_terms = ac

	@cherrypy.expose()
	def default(self,uid='1',typ='1',page='1',search='',topt='0',dopt='0',hopt='0'):
		return """
<head data-live-domain="jquery.com">
	<meta charset="utf-8">

	<title>News Feed - Search</title>

	<link rel="stylesheet" href="http://jqueryui.com/jquery-wp-content/themes/jquery/css/base.css?v=1">
	<link rel="stylesheet" href="http://jqueryui.com/jquery-wp-content/themes/jqueryui.com/style.css">

	<link rel="stylesheet" href="http://jquery.com/jquery-wp-content/themes/jquery/css/base.css?v=1">
	<link rel="stylesheet" href="http://jquery.com/jquery-wp-content/themes/jquery.com/style.css">

	<script src="http://jquery.com/jquery-wp-content/themes/jquery/js/modernizr.custom.2.6.2.min.js"></script>

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

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
					<input id="searchbar" type="text" name="search" value='"""+str(search)+"""' placeholder="Search">
					</div>
				</label>
			</form>
		</nav>

		<div id="content-wrapper" class="clearfix row">

			<div class="content-right twelve columns">
				<div id="content" style="width:75%">

					""" + self.get_search(uid,typ,page,search,topt,dopt,hopt) + """

					<div class="pagination">
						""" + self.search_pagination(uid,typ,page,search,topt,dopt,hopt) + """
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

	def search_pagination(self, uid, typ, page, search, topt, dopt ,hopt):

		string = ''
		for i in range(1,self.num_pages+1):
			if page == str(i):
				string += "<span class='page-numbers current'><b style=\"color:#909090;\">"+str(i)+"</b></span>\n"
			else:
				string += "<a class='page-numbers' href='/search/"+uid+"/"+typ+"/"+str(i)+"/"+search+"/"+topt+"/"+dopt+"/"+hopt+"'\"><b>"+str(i)+"</b></a>\n"

		return string

	def get_search(self, uid, typ, page, search, topt, dopt, hopt):
		uid = int(uid)
		page = int(page)

		searcher = self.index.searcher(weighting=scoring.TF_IDF())
		parser = MultifieldParser(['datetime','title','s_title','description','s_description','text','s_text','topics'],self.index.schema)
		parser.add_plugin(DateParserPlugin())

		myquery = parser.parse(' OR '.join((search.split())))

		if typ == '1':
			raw_results = searcher.search(myquery, limit=50)
			print raw_results[:]
			self.num_pages = min(len(raw_results[:])/10 + min(len(raw_results[:])%10,1),5)
			raw_results.fragmenter.surround = 30
			list_results = list(range((page-1)*10, min(len(raw_results[:]),page*10)))
		elif typ == '2':
			raw_results = searcher.search(myquery, limit=None)
			self.num_pages = min(len(raw_results[:])/10 + min(len(raw_results[:])%10,1),5)
			raw_results.fragmenter.surround = 30
			list_results = self.get_faceted(raw_results, uid, topt, dopt, hopt)[(page-1)*10:page*10]

		results = []
		max_score = 0
		for i in list_results:
			results.append({'urating':2,'view':0})
			results[-1]['id'] = int(raw_results[i]['id'])
			results[-1]['score'] = float(raw_results.score(i))
			if results[-1]['score'] > max_score: max_score = results[-1]['score']
			if raw_results[i].highlights("s_title") != '':
				results[-1]['s_title'] = raw_results[i].highlights("s_title")
			else: results[-1]['s_title'] = raw_results[i]["s_title"]
			if raw_results[i].highlights("s_description") != '':
				results[-1]['s_description'] = raw_results[i].highlights("s_description")
			else: results[-1]['s_description'] = raw_results[i]["s_description"]
			if raw_results[i].highlights("s_text") != '':
				results[-1]['s_text'] = raw_results[i].highlights("s_text",top=3).replace('...',' ... ')
			else: results[-1]['s_text'] = raw_results[i]["s_text"][:200] + ' ...'
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
		string = self.faceted_html(uid, search, topt, dopt, hopt)
		for r in results:
			string += '<table><tr style="border-bottom: 1px solid #666;"><td width="170px";>\n'
			string += '<img src="'+r['thumbnail']+'";""></td>'
			string += '<td><a href="/document/'+str(uid)+'/'+str(r['id'])+'" style="color:#505050;:hover{text-decoration:none;}">'
			string += '<h2 style="color:#808080;margin-bottom:5;">'+r['s_title']+'</h2></a>'
			string += '<h4 style="color:#808080;margin-bottom:5;">'+r['s_description']+'</h4>'
			string += '<p style="color:#808080;margin-bottom:5; font-size:15">'+r['s_text']+'</p>'
			string += '</td></tr></table>\n'

		return string

	def faceted_html(self, uid, search, topt, dopt, hopt):
		topics = ['Any topic','Business','Politics','Health','Education','Science & Environment','Technology',
		'Entertainment & Arts','Magazine','History','Consumer','Arts & Culture','Nature','Sports','Capital']
		documents = ['Any time','Last hour','Last day','Last week','Last month','Last year']
		historics = ['Any document','Viewed documents','Non-viewed documents']
		string = '<div class="dev-links" style="width: 100%;">\n'
		string += '<form method="post" class="searchform" action=\'/search/'+str(uid)+'/2/1/'+search+'\'>\n'
		string += '<select name="topt" style="font-size:15;background-color:#FFF;" onchange="this.form.submit()">'
		for i in range(15):
			string += '<option '
			if topt == str(i): string += 'selected '
			string += 'value="'+str(i)+'">'+topics[i]+'</option>\n'
		string += '</select>&nbsp&nbsp&nbsp\n'
		string += '<select name="dopt" style="font-size:15;background-color:#FFF;" onchange="this.form.submit()">'
		for i in range(6):
			string += '<option '
			if dopt == str(i): string += 'selected '
			string += 'value="'+str(i)+'">'+documents[i]+'</option>\n'
		string += '</select>&nbsp&nbsp&nbsp\n'
		string += '<select name="hopt" style="font-size:15;background-color:#FFF;" onchange="this.form.submit()">'
		for i in range(3):
			string += '<option '
			if hopt == str(i): string += 'selected '
			string += 'value="'+str(i)+'">'+historics[i]+'</option>\n'
		string += '</select>\n'
		string += '</form></div>\n'
		return string

	def get_faceted(self, raw_results, uid, topt, dopt, hopt):
		list_results = []
		ids = [int(r['id']) for r in raw_results[:]]

		database = connect('../Database/database.db')
		for i in range(len(ids)):
			if topt != '0':
				topics = []
				for row in database.execute('SELECT tpd_topic from tpc_doc where tpd_document = '+str(ids[i])):
					topics.append(str(row[0]))
				if topt not in topics:
					continue
			if dopt != '0':
				now_date = datetime.now()
				for row in database.execute('SELECT doc_datetime from documents where doc_id = '+str(ids[i])):
					doc_date = parser.parse(row[0])
				if dopt  == '1': delta = relativedelta(hours = 1)
				elif dopt  == '2': delta = relativedelta(days = 1)
				elif dopt  == '3': delta = relativedelta(weeks = 1)
				elif dopt  == '4': delta = relativedelta(months = 1)
				elif dopt  == '5': delta = relativedelta(years = 1)
				if doc_date < pytz.utc.localize(now_date-delta):
					continue
			if hopt != '0':
				viewed = '2'
				for row in database.execute('SELECT hst_rating from historics'+\
				' where hst_document = '+str(ids[i])+' and hst_user = '+str(uid)+';'):
					viewed = '1'
				if hopt != viewed:
					continue
			list_results.append(i)

		self.num_pages = min(len(list_results)/10 + min(len(list_results)%10,1),5)

		return list_results
