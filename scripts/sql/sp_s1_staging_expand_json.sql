CREATE OR REPLACE PROCEDURE staging.sp_s1_expand_json ()
LANGUAGE SQL
AS $$

	WITH expanded_json AS
	(
		SELECT
			snapshot_id,
			snapshot_timestamp,
			jsonb_array_elements(json_extract -> 'items') -> 'track' AS track_details
		FROM
			import.tbl_playlist_snapshot
	)
	INSERT INTO staging.tbl_playlist_snapshot
	SELECT
		snapshot_id,
		snapshot_timestamp,
		track_details ->> 'id' AS track_id,
		track_details ->> 'name' AS track_name,
		(track_details ->> 'duration_ms')::int AS duration_ms,
		(track_details ->> 'popularity')::int AS popularity,
		(track_details ->> 'artists')::jsonb AS artists,
		(track_details ->> 'album')::jsonb AS album
	FROM
		expanded_json

$$;