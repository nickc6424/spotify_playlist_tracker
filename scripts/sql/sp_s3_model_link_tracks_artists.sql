CREATE OR REPLACE PROCEDURE model.sp_s3_link_tracks_artists ()
LANGUAGE SQL
AS $$

    WITH expanded_json AS
    (
        SELECT
            track_id
            ,jsonb_array_elements(artists) AS artist
        FROM
            staging.tbl_playlist_snapshot
        WHERE
            snapshot_id  = (SELECT MAX(snapshot_id) FROM staging.tbl_playlist_snapshot)
    )
    MERGE INTO
        model.d_link_tracks_artists AS model
    USING
        (
            SELECT
                track_id
                ,artist ->> 'id' AS artist_id
            FROM 
                expanded_json
        ) AS latest
    ON
        model.track_id  = latest.track_id
        AND model.artist_id = latest.artist_id
    WHEN NOT MATCHED THEN
        INSERT (track_id, artist_id)
            VALUES
            (
                latest.track_id,
                latest.artist_id
            );

$$;