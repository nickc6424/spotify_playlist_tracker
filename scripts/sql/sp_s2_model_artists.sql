CREATE OR REPLACE PROCEDURE model.sp_s2_artists ()
LANGUAGE SQL
AS $$

    WITH expanded_json AS
    (
        SELECT
            snapshot_id
            ,jsonb_array_elements(artists) AS artists
        FROM
            staging.tbl_playlist_snapshot
    )
    MERGE INTO
        model.d_artists AS model
    USING
        (
            SELECT DISTINCT
                artists ->> 'id' as artist_id
                ,artists ->> 'name' as artist_name
            FROM
                expanded_json
            WHERE
                snapshot_id  = (SELECT MAX(snapshot_id) FROM staging.tbl_playlist_snapshot)
        ) AS latest
    ON
        model.artist_id  = latest.artist_id 
    WHEN MATCHED THEN
        UPDATE SET
            artist_name = latest.artist_name
    WHEN NOT MATCHED THEN
        INSERT (artist_id, artist_name)
            VALUES
            (
                latest.artist_id,
                latest.artist_name
            );

$$;