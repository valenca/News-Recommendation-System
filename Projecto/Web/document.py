import cherrypy
from cPickle import load
from gensim.models.ldamodel import LdaModel
from gensim import similarities
from gensim.corpora import Dictionary
from sqlite3 import connect
from operator import itemgetter
from dateutil import parser

class Document(object):

	def __init__(self, ac):
		with open('../TextMining/Topic/data.loc','rb') as f:
			load(f)
			self.data = load(f)
		with open('../TextMining/Topic/translator.loc','rb') as f:
			self.translator = load(f)
		self.index = similarities.MatrixSimilarity.load('../TextMining/Topic/index.loc')
		self.lda = LdaModel.load('../TextMining/Topic/lda.loc')
		self.dictionary = Dictionary().load("../TextMining/Topic/dic.loc")
		self.ac_terms = ac

	@cherrypy.expose
	def default(self, uid='1', did='-1'):
		if did == '-1':
			raise cherrypy.HTTPRedirect("/home/"+uid)
		return """
<head data-live-domain="jquery.com">
	<meta charset="utf-8">

	<title>News Feed - Documents</title>

	<script src='//jquery-star-rating-plugin.googlecode.com/svn/trunk/jquery.js' type="text/javascript"></script>
	<script src='//jquery-star-rating-plugin.googlecode.com/svn/trunk/jquery.rating.js' type="text/javascript" language="javascript"></script>
	<link href='//jquery-star-rating-plugin.googlecode.com/svn/trunk/jquery.rating.css' type="text/css" rel="stylesheet"/>

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
	
		.rating {
		  	unicode-bidi: bidi-override;
		  	direction: rtl;
		  	text-align: left;
		}
		.rating > span {
		  	display: inline-block;
		  	position: relative;
		  	width: 1.0em;
		}
		.rating > span:hover,
		.rating > span:hover ~ span {
		  	color: transparent;
		}
		.rating > span:hover:before,
		.rating > span:hover ~ span:before {
		   	content: "\\2605";
		   	position: absolute;
		   	#left: 0; 
		   	color: CornflowerBlue;
		}

	</style>

	<style media="screen" type="text/css">
		.ui-menu, .ui-menu-item a{
		color: #606060;
		border-radius: 10px;
		font-size:12px;
		width:333px;
	}
	</style>

	<script>
	function rate() {
		alert('qwer');
	}
	</script>

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

					""" + self.get_document(uid, did) + """

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

	def get_document(self, uid, did):
		uid = int(uid)
		did = int(did)

		database = connect('../Database/database.db')

		doc={'urating':-1,'view':0}
		for row in database.execute('SELECT doc_datetime,doc_link,doc_thumbnail,doc_title,doc_description,'+\
			'doc_text,doc_rating,doc_nviews FROM documents where doc_id = '+str(did)+';'):
			doc['datetime']=parser.parse(str(row[0])).strftime('%d/%m/%Y - %H:%M:%S')
			doc['link'] = str(row[1])
			doc['thumbnail'] = str(row[2])
			doc['title'] = str(row[3])
			doc['description'] = str(row[4])
			doc['text'] = str(row[5])
			doc['rating'] = row[6]
			doc['nviews'] = row[7]

		doc['topics'] = []
		topics = []
		for row in database.execute('SELECT tpc_id,tpc_name FROM topics,tpc_doc where tpd_document = '+str(did)+\
			' and tpd_topic = tpc_id;'):
			topics.append(row[0])
			doc['topics'].append(str(row[1]))

		doc['entities'] = []
		for row in database.execute('SELECT ent_entity FROM entities where ent_document = '+str(did)+';'):
			doc['entities'].append(str(row[0]))

		for row in database.execute('SELECT hst_rating FROM historics where hst_document = '+\
			str(did)+' and hst_user = '+str(uid)+';'):
			doc['urating'] = row[0]
			doc['view'] = 1

		if doc['view'] == 0:
			database.execute('UPDATE users set usr_nviews = usr_nviews+1 where usr_id = '+str(uid)+';')
			database.execute('UPDATE documents set doc_nviews = doc_nviews+1 where doc_id = '+str(did)+';')
			database.execute('INSERT INTO historics VALUES ('+str(uid)+','+str(did)+',-1);')
			for t in topics:
				database.execute('UPDATE tpc_preferences set tpp_nviews = tpp_nviews+1 where tpp_topic = '+str(t)+' and tpp_user = '+str(uid)+';')
		
		string = '<div class="dev-links" style="width: 35%;">\n'
		string += '<h3><a href="'+doc['link']+'" style="color:303030;">Source link</a></h3>\n'
		string += '<h3 style="color:303030;margin-bottom:5;">Rate this document:</h3>\n'
		string += self.rating_stars(doc['urating'])
		string += '<br><br><h3 style="color:303030;margin-bottom:5;">Sugested documents:</h3><ul>\n'
		string += self.sugested_documents(database, uid, did)
		string += '</ul><br><h3 style="color:303030;margin-bottom:5;">Tags:</h3><ul><li>\n'
		string += ', '.join(['<a href="/tag/'+str(uid)+'/'+t+'" style="color:303030;">'+t+'</a>' for t in doc['entities']])
		string += '</li></ul></div>\n'

		string += '<p style="color:#808080;float:left">'+doc['datetime']+'</p>\n'
		string += '<p align="right" style="color:#808080;float:right;">'+' | '.join(doc['topics'])+'</p>\n'
		string += '<div style="clear:left;"></div>\n'
		string += '<h1>'+doc['title']+'</h1>\n'

		string += '<table style="margin: 0em 0em"><tr style="border-bottom:15px solid #fff;background-color:#fff">'
		string += '<td width="170px";>'
		string += '<img src="'+doc['thumbnail']+'" style="vertical-align=middle;" align="left"></td>'
		string += '<td><p style="font-weight:bold;font-size:15;margin-bottom:0;">'+doc['text'].split('\n')[0]+'</p>\n'
		string += '</td></tr></table>\n'
		for p in doc['text'].split('\n')[1:]:
			string += '<p style="font-size:15;margin-bottom: 8px;">'+p+'</p>'

		return string

	def sugested_documents(self, database, uid, did):
		doc = self.data[did]

		vec_bow = self.dictionary.doc2bow(doc)
		vec_lda = self.lda[vec_bow] 
		sims = self.index[vec_lda]
		sims = [self.translator[s[0]] for s in sorted(enumerate(sims),key=lambda item: -item[1])[:11] if self.translator[s[0]] != did][:10]
		
		string = ''
		for s in sims:
			for row in database.execute('SELECT doc_title FROM documents where doc_id = '+str(s)+';'):
				string += '<li><a href="/document/'+str(uid)+'/'+str(s)+'" style="color:303030;">'+str(row[0])+'</a></li>\n'
		return string	

	def rating_stars(self, urating):
		if urating == -1: urating = 0;
		string = ''
		#return '<div class="rating" style="font-size:25px">' + (5-urating) * '<span>&#9734</span>' + urating *'<span>&#9733</span>'+'&nbsp&nbsp</div>'
		for i in range(1,6):
			if i == urating:
				string += '<input type="radio" class="star" checked="checked" onclick="rate()"/>'
			else:
				string += '<input type="radio" class="star" onclick="rate()"/>'
		return string
