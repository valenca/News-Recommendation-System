import cherrypy
from sqlite3 import connect
import simplejson

class Script(object):

	@cherrypy.expose
	def default(self):
		cl = cherrypy.request.headers['Content-Length']
		print cl
		rawbody = cherrypy.request.body.read(int(cl))
		rating, uid, did = rawbody.split()

		database = connect('../Database/database.db')

		for row in database.execute('SELECT hst_rating from historics where hst_user = '+str(uid)+\
			' and hst_document = '+str(did)+';'):
			p_rating = row[0]
		for row in database.execute('SELECT doc_rating,doc_nratings from documents where doc_id = '+str(did)+';'):
			d_rating = row[0]
			d_nratings = row[1]
		for row in database.execute('SELECT tpp_rating,tpp_nratings from tpc_preferences where tpp_user = '+str(uid)+';'):
			t_rating = row[0]
			t_nratings = row[1]

		database.execute('UPDATE historics set hst_rating = '+str(rating)+' where hst_user = '+str(uid)+\
			' and hst_document = '+str(did)+';')

		if p_rating == -1:
			d_rating = d_rating * (float(d_nratings)/(d_nratings+1)) + int(rating) * (1.0/(d_nratings+1))
			d_nratings += 1
			t_rating = t_rating * (float(t_nratings)/(t_nratings+1)) + int(rating) * (1.0/(t_nratings+1))
			t_nratings += 1
		else:
			d_rating += (int(rating) - p_rating) * (1.0/d_nratings)
			t_rating += (int(rating) - p_rating) * (1.0/t_nratings)
		
		database.execute('UPDATE documents set doc_rating = '+str(d_rating)+',doc_nratings = '+str(d_nratings)+\
			' where doc_id = '+str(did)+';')
		database.execute('UPDATE tpc_preferences set tpp_rating = '+str(t_rating)+',tpp_nratings = '+str(t_nratings)+\
			' where tpp_user = '+str(uid)+';')

		database.commit()

		return ''
