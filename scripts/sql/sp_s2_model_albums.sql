CREATE OR REPLACE PROCEDURE model.sp_s2_albums ()
LANGUAGE SQL
AS $$

    MERGE INTO
        model.d_albums AS model
    USING
        (
            SELECT DISTINCT
                snapshot_id
                ,album ->> 'id' as album_id
                ,album ->> 'name' as album_name
                ,CASE
                    WHEN NOT album ->> 'release_date' ~ '^\d{1,4}-\d{2}-\d{2}$' THEN NULL
                    ELSE (album ->> 'release_date')::date
                END AS release_date
                ,(album ->> 'total_tracks')::int as total_tracks
            FROM
                staging.tbl_playlist_snapshot
            WHERE
                snapshot_id  = (SELECT MAX(snapshot_id) FROM staging.tbl_playlist_snapshot)
        ) AS latest
    ON
        model.album_id  = latest.album_id 
    WHEN MATCHED THEN
        UPDATE SET
            album_name = latest.album_name,
            release_date  = latest.release_date,
            total_tracks = latest.total_tracks
    WHEN NOT MATCHED THEN
        INSERT (album_id, album_name, release_date, total_tracks)
            VALUES
            (
                latest.album_id,
                latest.album_name,
                latest.release_date,
                latest.total_tracks
            );

$$;