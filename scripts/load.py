import psycopg2
from psycopg2.sql import SQL, Identifier
from helper_functions import read_config
import json


def read_db_connection():
    """Reads the database connection details from the configuration file."""
    return {
        "host": read_config("secrets.cfg", "database", "host"),
        "user": read_config("secrets.cfg", "database", "user"),
        "password": read_config("secrets.cfg", "database", "password"),
        "dbname": read_config("secrets.cfg", "database", "dbname"),
        "port": read_config("secrets.cfg", "database", "port"),
    }


def execute_query(sql: str, vars=None):
    """Executes a SQL string against the database.
    Parameters:
        sql: The SQL string to execute
        vars: Optional parameters to be passed into the SQL string
    """
    with psycopg2.connect(**read_db_connection()) as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, vars)
        except Exception as e:
            # Rollback changes if exception
            conn.rollback()
            raise e
        finally:
            # Commit changes to the database
            conn.commit()

    # Close the connection - context manager won't do this for psycopg2
    conn.close()


def get_sql_from_script(filepath: str) -> str:
    """Extracts the contents of a SQL script and returns it as a string."""
    with open(filepath, "r") as script:
        sql = script.read()
    return sql


def execute_query_from_script(sql_filepath: str, vars=None):
    """Executes a SQL script against the database.
    Parameters:
        sql_filepath: The filepath to the SQL script
        vars: Optional parameters to be passed into the SQL script
    """
    sql = get_sql_from_script(sql_filepath)
    execute_query(sql, vars)


def create_schema(schemaName: str):
    """Creates a schema in the database."""
    sql = get_sql_from_script("./scripts/sql/create_schema.sql")
    sql_formatted = SQL(sql).format(Identifier(schemaName))
    execute_query(sql_formatted)


def execute_stored_procedure(schema: str, procedure_name: str):
    """Executes a stored procedure in the database, assuming no input parameters."""
    sql = get_sql_from_script("./scripts/sql/call_stored_procedure.sql")
    sql_formatted = SQL(sql).format(Identifier(schema), Identifier(procedure_name))
    execute_query(sql_formatted)


def truncate_table(schema: str, table_name: str):
    """Truncates a database table."""
    sql = get_sql_from_script("./scripts/sql/truncate_table.sql")
    sql_formatted = SQL(sql).format(Identifier(schema), Identifier(table_name))
    execute_query(sql_formatted)


def setup_database():
    """Creates all the database objects needed to store and process the data."""
    # Create schemas
    create_schema("import")
    create_schema("staging")
    create_schema("model")

    # Create tables
    execute_query_from_script("./scripts/sql/ct_import_playlist_snapshot.sql")
    execute_query_from_script("./scripts/sql/ct_staging_playlist_snapshot.sql")
    execute_query_from_script("./scripts/sql/ct_model_d_albums.sql")
    execute_query_from_script("./scripts/sql/ct_model_d_artists.sql")
    execute_query_from_script("./scripts/sql/ct_model_d_link_track_artist.sql")
    execute_query_from_script("./scripts/sql/ct_model_d_tracks.sql")
    execute_query_from_script("./scripts/sql/ct_model_f_snapshots.sql")

    # Create stored procedures
    execute_query_from_script("./scripts/sql/sp_s1_staging_expand_json.sql")
    execute_query_from_script("./scripts/sql/sp_s2_model_tracks.sql")
    execute_query_from_script("./scripts/sql/sp_s2_model_albums.sql")
    execute_query_from_script("./scripts/sql/sp_s2_model_artists.sql")
    execute_query_from_script("./scripts/sql/sp_s3_model_link_tracks_artists.sql")
    execute_query_from_script("./scripts/sql/sp_s4_model_snapshots.sql")


def main(data_to_load: dict):
    """Loads API data into Postgres database.
    Parameters:
        data_to_load: The data to be loaded into the database
    """
    # Create the landing table if it doesn't exist
    create_schema("import")
    execute_query_from_script("./scripts/sql/ct_import_playlist_snapshot.sql")

    # Insert the data into the landing table
    execute_query_from_script("./scripts/sql/insert_into_playlist_snapshot.sql", (json.dumps(data_to_load),))

    # Call the transformation stored procedures
    execute_stored_procedure("staging", "sp_s1_expand_json")
    execute_stored_procedure("model", "sp_s2_tracks")
    execute_stored_procedure("model", "sp_s2_albums")
    execute_stored_procedure("model", "sp_s2_artists")
    execute_stored_procedure("model", "sp_s3_link_tracks_artists")
    execute_stored_procedure("model", "sp_s4_snapshots")

    # Truncate staging tables
    truncate_table("import", "tbl_playlist_snapshot")
    truncate_table("staging", "tbl_playlist_snapshot")
