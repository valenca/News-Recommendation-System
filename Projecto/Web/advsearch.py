import cherrypy
from sqlite3 import connect
from operator import itemgetter
from dateutil import parser

class AdvSearch(object):

	@cherrypy.expose
	def default(self, uid='1'):
		return """
<head data-live-domain="jquery.com">
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

	<title>News Feed - Advanced Search</title>

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

					<h1>Advanced Search</h1>

					""" + self.get_advsearch_form(uid) + """

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

	def get_advsearch_form(self, uid='1'):
		uid = int(uid)
		
		string = '<form method="post" class="searchform" action="/search/"""+str(uid)+"""/1">'
		string += '<table><tr style="border-bottom:0;background-color:#fff">'
		string += '<td><h2 style="margin-bottom:0;">Topic: </h2></td>'
		string += '<td><select style="font-size:15">'
		string += '<option value="1">Business</option>'
		string += '<option value="2">Politics</option>'
		string += '<option value="3">Health</option>'
		string += '<option value="4">Education</option>'
		string += '<option value="5">Science & Environment</option>'
		string += '<option value="6">Technology</option>'
		string += '<option value="7">Entertainment & Arts</option>'
		string += '<option value="8">Magazine</option>'
		string += '<option value="9">History</option>'
		string += '<option value="10">Consumer</option>'
		string += '<option value="11">Arts & Culture</option>'
		string += '<option value="12">Nature</option>'
		string += '<option value="13">Sports</option>'
		string += '<option value="14">Capital</option>'
		string += '</select></td></tr><tr style="border-bottom:0;background-color:#fff">'
		string += '<td><h2 style="margin-bottom:0;">Date: </h2></td>'
		string += '<td><table style="margin: 0em -0.5em;"><tr style="border-bottom:0;background-color:#fff">'
		string += '<td><h5 style="margin-bottom:0;">From:</h5>'
		string += '<input type="date" name="fdate" style="font-size:15"></td>'
		string += '<td><h5 style="margin-bottom:0;">To:</h5>'
		string += '<input type="date" name="tdate" style="font-size:15"></td>'
		string += '</tr></table></td></tr><tr style="border-bottom:0;background-color:#fff">'
		string += '<td><h2 style="margin-bottom:0;">Title:</h2></td>'
		string += '</tr><tr style="border-bottom:0;background-color:#fff">'
		string += '<td><h2 style="margin-bottom:0;">Description:</h2></td>'
		string += '</tr><tr style="border-bottom:0;background-color:#fff">'
		string += '<td><h2 style="margin-bottom:0;">Text:</h2></td>'
		string += '</tr><tr style="border-bottom:0;background-color:#fff">'
		string += '</table></form>'

		return string
