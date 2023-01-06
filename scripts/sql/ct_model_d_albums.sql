CREATE TABLE IF NOT EXISTS model.d_albums
(
	album_id varchar(22) NOT NULL,
	album_name text NOT NULL,
	release_date date NULL,
	total_tracks smallint NOT NULL
);