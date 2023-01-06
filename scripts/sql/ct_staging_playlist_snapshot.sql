CREATE TABLE IF NOT EXISTS staging.tbl_playlist_snapshot
(
    snapshot_id int NOT NULL,
    snapshot_timestamp timestamp NOT NULL,
    track_id varchar(22) NOT NULL,
    track_name text NOT NULL,
    duration_ms int NOT NULL,
    popularity smallint NOT NULL,
    artists jsonb NOT NULL,
    album jsonb NOT NULL
);