import cherrypy

class Home(object):

	@cherrypy.expose
	def index(self, uid=0):
		raise cherrypy.HTTPRedirect("/home/1")

	@cherrypy.expose
	def home(self, uid=1):
		return """
<head data-live-domain="jquery.com">
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

	<title>News Feed</title>

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
				""" + self.get_home_docs(uid)+\
		"""
<h2><a href="http://jqueryui.com/themeroller" style="color:#404040;">What's New in jQuery UI 1.10?</a></h2>

<p>jQuery UI 1.10 includes dozens of bug fixes and improved accessibility.
In addition, the dialog and progressbar widgets have undergone
<a href="http://blog.jqueryui.com/2011/03/api-redesigns-the-past-present-and-future/">API redesigns</a>,
making them easier to use and creating more consistency across plugins.</p>

<p>Interested in the full details of what changed? Check out the
<a href="/upgrade-guide/1.10/">1.10 upgrade guide</a>,
<a href="/changelog/1.10.0/">1.10.0 changelog</a>,
<a href="/changelog/1.10.1/">1.10.1 changelog</a>,
<a href="/changelog/1.10.2/">1.10.2 changelog</a>,
<a href="/changelog/1.10.3/">1.10.3 changelog</a>, and 
<a href="/changelog/1.10.4/">1.10.4 changelog</a>.</p>

<hr class="dots"/>
<hr class="dots"/>
<h2>Dive In!</h2>

<p>jQuery UI is built for designers and developers alike. We've designed
all of our plugins to get you up and running quickly while being flexible
enough to evolve with your needs and solve a plethora of use cases. If
you're new to jQuery UI, check out our
<a href="http://learn.jquery.com/jquery-ui/getting-started/">getting started
guide</a> and <a href="http://learn.jquery.com/jquery-ui/">other tutorials</a>.
Play around with the <a href="/demos/">demos</a> and read through the
<a href="http://api.jqueryui.com/">API documentation</a> to get an idea
of what's possible.</p>

<hr class="dots"/>
<h2>Dive In!</h2>

<p>jQuery UI is built for designers and developers alike. We've designed
all of our plugins to get you up and running quickly while being flexible
enough to evolve with your needs and solve a plethora of use cases. If
you're new to jQuery UI, check out our
<a href="http://learn.jquery.com/jquery-ui/getting-started/">getting started
guide</a> and <a href="http://learn.jquery.com/jquery-ui/">other tutorials</a>.
Play around with the <a href="/demos/">demos</a> and read through the
<a href="http://api.jqueryui.com/">API documentation</a> to get an idea
of what's possible.</p>

<hr class="dots"/>
<h2>Dive In!</h2>

<p>jQuery UI is built for designers and developers alike. We've designed
all of our plugins to get you up and running quickly while being flexible
enough to evolve with your needs and solve a plethora of use cases. If
you're new to jQuery UI, check out our
<a href="http://learn.jquery.com/jquery-ui/getting-started/">getting started
guide</a> and <a href="http://learn.jquery.com/jquery-ui/">other tutorials</a>.
Play around with the <a href="/demos/">demos</a> and read through the
<a href="http://api.jqueryui.com/">API documentation</a> to get an idea
of what's possible.</p>

				</div>

				<div id="sidebar" class="widget-area" role="complementary" width=10px>
				<aside class="widget">
					<h3 class="widget-title">Topics</h3>
					<ul>
						<li><a href="https://jqueryui.com/draggable/">Business</a></li>
						<li><a href="https://jqueryui.com/droppable/">Politics</a></li>
						<li><a href="https://jqueryui.com/resizable/">Health</a></li>
						<li><a href="https://jqueryui.com/selectable/">Science & Environment</a></li>
						<li><a href="https://jqueryui.com/sortable/">Technology</a></li>
						<li><a href="https://jqueryui.com/sortable/">Entertainment & Arts</a></li>
						<li><a href="https://jqueryui.com/sortable/">Magazine</a></li>
						<li><a href="https://jqueryui.com/sortable/">Sports</a></li>
						<li><a href="https://jqueryui.com/sortable/">History</a></li>
						<li><a href="https://jqueryui.com/sortable/">Capital</a></li>
						<li><a href="https://jqueryui.com/sortable/">Nature</a></li>
						<li><a href="https://jqueryui.com/sortable/">Consumer</a></li>
						<li><a href="https://jqueryui.com/sortable/">Culture</a></li>
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

	def get_home_docs(self, uid=1):
		from sqlite3 import connect
		database = connect('../Database/database.db')

		for row in database.execute('SELECT count(*) FROM documents;'):
			ndocs = row[0]
			docs = [{} for i in range(ndocs)]
		for did in range(1,ndocs+1):

			for row in database.execute('SELECT doc_id,doc_rating,doc_nviews from documents'+\
				' where doc_id = '+str(did)+';'):
				docs[did-1]['id'] = row[0]
				docs[did-1]['rating'] = row[1]
				docs[did-1]['views'] = row[2]
			for row in database.execute('SELECT hst_rating,hst_view from historics'+\
				' where hst_document = '+str(did)+' and hst_user = '+str(uid)+';'):
				docs[did-1]['urating'] = row[0]
				docs[did-1]['view'] = row[1]
			for row in database.execute('SELECT usr_nviews, 

		return ''

if __name__ == '__main__':
	cherrypy.quickstart(Home())
