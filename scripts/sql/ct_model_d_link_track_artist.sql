CREATE TABLE IF NOT EXISTS model.d_link_tracks_artists
(
	link_id serial PRIMARY KEY,
	track_id varchar(22) NOT NULL,
	artist_id varchar(22) NOT NULL
);