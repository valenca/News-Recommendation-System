CREATE TABLE users (
	usr_id INTEGER NOT NULL,
	usr_name TEXT NOT NULL,
	usr_username TEXT NOT NULL,
	usr_password TEXT NOT NULL,
	usr_nviews INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY (usr_id)
);

CREATE TABLE documents (
	doc_id INTEGER NOT NULL,
	doc_datetime DATETIME NOT NULL,
	doc_link TEXT NOT NULL,
	doc_thumbnail TEXT NOT NULL,
	doc_title TEXT NOT NULL,
	doc_description TEXT NOT NULL,
	doc_text TEXT NOT NULL,
	doc_topic INTEGER NOT NULL REFERENCES topics(tpc_id),
	doc_rating REAL NOT NULL DEFAULT 2.5,
	doc_nratings INTEGER NOT NULL DEFAULT 0,
	doc_nviews INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY (doc_id)
);

CREATE TABLE topics (
	tpc_id INTEGER NOT NULL,
	tpc_name TEXT NOT NULL,
	PRIMARY KEY (tpc_id)
);

CREATE TABLE feeds (
	fds_id INTEGER NOT NULL,
	fds_topic INTEGER NOT NULL REFERENCES topics(tpc_id),
	fds_link TEXT NOT NULL,
	PRIMARY KEY (fds_id)
);

CREATE TABLE tags (
	tgs_id INTEGER NOT NULL,
	tgs_tag TEXT NOT NULL,
	PRIMARY KEY (tgs_id)
);

CREATE TABLE marks (
	mrk_tag INTEGER NOT NULL REFERENCES tags(tgs_id),
	mrk_document INTEGER NOT NULL REFERENCES documents(doc_id),
	PRIMARY KEY (mrk_tag, mrk_document)
);
 

CREATE TABLE historics (
	hst_user INTEGER NOT NULL REFERENCES users(usr_id),
	hst_document INTEGER NOT NULL REFERENCES documents(doc_id),
	hst_rating INTEGER NOT NULL DEFAULT -1,
	hst_view INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY (hst_user, hst_document)
);

CREATE TABLE tpc_preferences (
	tpp_user INTEGER NOT NULL REFERENCES users(usr_id),
	tpp_topic INTEGER NOT NULL REFERENCES topics(tpc_id),
	tpp_nviews INTEGER NOT NULL DEFAULT 0,
	tpp_rating REAL NOT NULL DEFAULT 2.5,
	tpp_nratings INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY (tpp_user, tpp_topic)
);

CREATE TABLE tgs_preferences (
	tgs_user INTEGER NOT NULL REFERENCES users(usr_id),
	tgs_tag INTEGER NOT NULL REFERENCES tags(tgs_id),
	tgs_nviews INTEGER NOT NULL DEFAULT 0,
	tgs_rating REAL NOT NULL DEFAULT 2.5,
	tgs_nratings INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY (tgs_user, tgs_tag)
);
