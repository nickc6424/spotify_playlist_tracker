CREATE TABLE IF NOT EXISTS model.f_snapshots
(
    snapshot_id int NOT NULL,
    snapshot_timestamp timestamp NOT NULL,
    track_id varchar(22) NOT NULL,
    popularity smallint NOT NULL
);