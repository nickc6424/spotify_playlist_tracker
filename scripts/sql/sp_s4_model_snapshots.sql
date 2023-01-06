CREATE OR REPLACE PROCEDURE model.sp_s4_snapshots ()
LANGUAGE SQL
AS $$

    MERGE INTO
        model.f_snapshots AS model
    USING
        (
            SELECT 
                snapshot_id,
                snapshot_timestamp,
                track_id,
                popularity
            FROM 
                staging.tbl_playlist_snapshot 
            WHERE
                snapshot_id  = (SELECT MAX(snapshot_id) FROM staging.tbl_playlist_snapshot)
        ) AS latest
    ON
        model.snapshot_id  = latest.snapshot_id
        AND model.track_id = latest.track_id
    WHEN NOT MATCHED THEN
        INSERT (snapshot_id, snapshot_timestamp, track_id, popularity)
            VALUES
            (
                latest.snapshot_id,
                latest.snapshot_timestamp,
                latest.track_id,
                latest.popularity
            );

$$;