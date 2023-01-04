CREATE TABLE IF NOT EXISTS spotify.import.tbl_playlist_snapshot
(
    batch_id serial PRIMARY KEY,
    json_extract jsonb NOT NULL,
    inserted_at timestamp NOT NULL DEFAULT now()
);