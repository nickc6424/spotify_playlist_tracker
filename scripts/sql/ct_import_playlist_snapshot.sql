CREATE TABLE IF NOT EXISTS import.tbl_playlist_snapshot
(
    snapshot_id serial PRIMARY KEY,
    json_extract jsonb NOT NULL,
    snapshot_timestamp timestamp NOT NULL DEFAULT now()
);