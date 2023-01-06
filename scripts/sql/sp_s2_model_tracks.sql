CREATE OR REPLACE PROCEDURE model.sp_s2_tracks ()
LANGUAGE SQL
AS $$

    MERGE INTO
        model.d_tracks AS model
    USING
        (
            SELECT
                track_id,
                track_name,
                duration_ms
            FROM
                staging.tbl_playlist_snapshot
            WHERE
	            snapshot_id  = (SELECT MAX(snapshot_id) FROM staging.tbl_playlist_snapshot)
        ) AS latest
    ON
        model.track_id  = latest.track_id 
    WHEN MATCHED THEN
        UPDATE SET
            track_name = latest.track_name,
            duration_ms  = latest.duration_ms
    WHEN NOT MATCHED THEN
        INSERT (track_id, track_name, duration_ms)
            VALUES
            (
                latest.track_id,
                latest.track_name,
                latest.duration_ms
            );

$$;