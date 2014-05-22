from sqlite3 import connect
from random import sample, random, choice
import urllib2

with open('firstnames','r') as f: firstnames = list(set([line[:-1] for line in f]))
with open('lastnames','r') as f: lastnames = list(set([line[:-1] for line in f]))

database = connect('../Database/database.db')
for row in database.execute('SELECT count(*) from users;'):
	total_usrs = row[0]
database.close()

for i in range(total_usrs+1,total_usrs+1+10):
	print i

	fn = choice(firstnames)
	ln = choice(lastnames)
	database = connect('../Database/database.db')
	database.execute('INSERT into users (usr_name, usr_username,usr_password) values '+\
		'(\''+fn+' '+ln+'\',\''+fn+'\',\''+ln+'\');')
	for j in range(1,15):
		database.execute('INSERT into tpc_preferences (tpp_user, tpp_topic) values '+\
		'('+str(i)+','+str(j)+');')
	for row in database.execute('SELECT count(*) from documents;'):
		total_docs = row[0]
	database.commit()
	database.close()

	docs = sample(list(range(1,total_docs+1)),250)

	for doc in docs:
		response = urllib2.urlopen('http://127.0.0.1:8080/document/'+str(i)+'/'+str(doc))
		if random() < 0.5:
			rating = choice([1,2,3,4,5])

			database = connect('../Database/database.db')

			for row in database.execute('SELECT hst_rating from historics where hst_user = '+str(i)+\
				' and hst_document = '+str(doc)+';'):
				p_rating = row[0]
			for row in database.execute('SELECT doc_rating,doc_nratings from documents where doc_id = '+str(doc)+';'):
				d_rating = row[0]
				d_nratings = row[1]
			for row in database.execute('SELECT tpp_rating,tpp_nratings from tpc_preferences where tpp_user = '+str(i)+';'):
				t_rating = row[0]
				t_nratings = row[1]

			database.execute('UPDATE historics set hst_rating = '+str(rating)+' where hst_user = '+str(i)+\
				' and hst_document = '+str(doc)+';')

			if p_rating == -1:
				d_rating = d_rating * (float(d_nratings)/(d_nratings+1)) + int(rating) * (1.0/(d_nratings+1))
				d_nratings += 1
				t_rating = t_rating * (float(t_nratings)/(t_nratings+1)) + int(rating) * (1.0/(t_nratings+1))
				t_nratings += 1
			else:
				d_rating += (int(rating) - p_rating) * (1.0/d_nratings)
				t_rating += (int(rating) - p_rating) * (1.0/t_nratings)
			
			database.execute('UPDATE documents set doc_rating = '+str(d_rating)+',doc_nratings = '+str(d_nratings)+\
				' where doc_id = '+str(doc)+';')
			database.execute('UPDATE tpc_preferences set tpp_rating = '+str(t_rating)+',tpp_nratings = '+str(t_nratings)+\
				' where tpp_user = '+str(i)+';')

			database.commit()
			database.close()

