CREATE TABLE users (
	u_id INTEGER NOT NULL,
	u_name TEXT NOT NULL,
	u_username TEXT NOT NULL,
	u_password TEXT NOT NULL,
	PRIMARY KEY (u_id)
);

CREATE TABLE news (
	n_id INTEGER NOT NULL,
	n_datetime DATETIME NOT NULL,
	n_link TEXT NOT NULL,
	n_thumbnail TEXT NOT NULL,
	n_title TEXT NOT NULL,
	n_description TEXT NOT NULL,
	n_text TEXT NOT NULL,
	n_topic INTEGER NOT NULL REFERENCES topics(t_id),
	n_rating REAL NOT NULL,
	n_total_ratings INTEGER NOT NULL,
	n_total_views INTEGER NOT NULL,
	PRIMARY KEY (n_id)
);

CREATE TABLE topics (
	t_id INTEGER NOT NULL,
	t_name TEXT NOT NULL,
	PRIMARY KEY (t_id)
);

CREATE TABLE evaluations (
	e_user INTEGER NOT NULL REFERENCES users(u_id),
	e_news INTEGER NOT NULL REFERENCES news(n_id),
	e_rating INTEGER NOT NULL,
	PRIMARY KEY (e_user, e_news)
);

CREATE TABLE views (
	v_user INTEGER NOT NULL REFERENCES users(u_id),
	v_news INTEGER NOT NULL REFERENCES news(n_id),
	PRIMARY KEY (v_user, v_news)
);

CREATE TABLE recommendations (
	r_user INTEGER NOT NULL REFERENCES users(u_id),
	r_news INTEGER NOT NULL REFERENCES news(n_id),
	r_rating REAL NOT NULL,
	PRIMARY KEY (r_user, r_news)
);

CREATE TABLE preferences (
	p_user INTEGER NOT NULL REFERENCES users(u_id),
	p_topic INTEGER NOT NULL REFERENCES topics(t_id),
	p_rating REAL NOT NULL,
	PRIMARY KEY (p_user, p_topic)
);

CREATE TABLE feeds (
	f_id INTEGER NOT NULL,
	f_topic INTEGER NOT NULL REFERENCES topics(t_id),
	f_link TEXT NOT NULL,
	PRIMARY KEY (f_id)
);
