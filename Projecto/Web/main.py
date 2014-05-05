import cherrypy

class Root(object):

	@cherrypy.expose
	def index(self):
		return """
<head data-live-domain="jqueryui.com">
	<meta charset="utf-8">

	<title>News Feed</title>

	<link rel="stylesheet" href="http://jqueryui.com/jquery-wp-content/themes/jquery/css/base.css?v=1">
	<link rel="stylesheet" href="http://jqueryui.com/jquery-wp-content/themes/jqueryui.com/style.css">
	<link rel="stylesheet" href="http://jquery.com/jquery-wp-content/themes/jquery/css/base.css?v=1">
	<link rel="stylesheet" href="http://jquery.com/jquery-wp-content/themes/jquery.com/style.css">

	<script src="http://jqueryui.com/jquery-wp-content/themes/jquery/js/plugins.js"></script>
	<script src="http://jqueryui.com/jquery-wp-content/themes/jquery/js/main.js"></script>
	<script src="http://jquery.com/jquery-wp-content/themes/jquery/js/plugins.js"></script>
	<script src="http://jquery.com/jquery-wp-content/themes/jquery/js/main.js"></script>

	<script src="//use.typekit.net/wde1aof.js"></script>
	<script>try{Typekit.load();}catch(e){}</script>

	<script type='text/javascript' src='http://jqueryui.com/wp-includes/js/comment-reply.min.js?ver=3.8'></script>
	<script type='text/javascript' src='http://jquery.com/wp-includes/js/comment-reply.min.js?ver=3.8'></script>

</head>
<body class="jquery home page page-id-5 page-template page-template-page-fullwidth-php page-slug-index single-author singular">

	<div id="container">
		<div id="logo-events" class="constrain clearfix">
			<h2> </h2>
		</div>

		<nav id="main" class="constrain clearfix">
			<div class="menu-top-container">
				<ul id="menu-top" class="menu">
					<li class="menu-item"><a href="http://jqueryui.com/demos/">Home</a></li>
					<li class="menu-item"><a href="http://jqueryui.com/download">Recommended</a></li>
					<li class="menu-item"><a href="http://api.jqueryui.com/">API Documentation</a></li>
					<li class="menu-item"><a href="http://jqueryui.com/themeroller">Themes</a></li>
					<li class="menu-item"><a href="http://jqueryui.com/development">Development</a></li>
					<li class="menu-item"><a href="http://jqueryui.com/support">Support</a></li>
					<li class="menu-item"><a href="http://blog.jqueryui.com/">Blog</a></li>
					<li class="menu-item"><a href="http://jqueryui.com/about">About</a></li>
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

<div class="dev-links">
	<h3>Developer Links</h3>
	<ul>
		<li><a href="https://github.com/jquery/jquery-ui">Source Code (GitHub)</a></li>
		<li><a href="http://code.jquery.com/ui/jquery-ui-git.js">jQuery UI Git (WIP Build)</a>
			<ul>
				<li><a href="http://code.jquery.com/ui/jquery-ui-git.css">Theme (WIP Build)</a></li>
			</ul>
		</li>
		<li><a href="http://bugs.jqueryui.com/">Bug Tracker</a>
			<ul>
				<li><a href="http://bugs.jqueryui.com/newticket/">Submit a New Bug Report</a></li>
			</ul>
		</li>
		<li><a href="http://forum.jquery.com/">Discussion Forum</a>
			<ul>
				<li><a href="http://forum.jquery.com/using-jquery-ui/">Using jQuery UI</a></li>
				<li><a href="http://forum.jquery.com/developing-jquery-ui/">Developing jQuery UI</a></li>
			</ul>
		</li>
		<li><a href="http://wiki.jqueryui.com/">Development Planning Wiki</a></li>
		<li><a href="http://wiki.jqueryui.com/Roadmap/">Roadmap</a></li>
		<li><a href="/browser-support/">Browser Support</a></li>
		<li><a href="/download/all/">Previous Releases</a>
			<ul>
				<li><a href="/changelog/">Changelogs</a></li>
				<li><a href="/upgrade-guide/">Upgrade Guides</a></li>
			</ul>
		</li>
	</ul>
</div>
		
<h2><a href="http://jqueryui.com/themeroller" style="text-decoration:none;color: #404040;">What's New in jQuery UI 1.10?</a></h2>

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


if __name__ == '__main__':
	cherrypy.quickstart(Root())
