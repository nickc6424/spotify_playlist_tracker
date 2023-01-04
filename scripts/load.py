import psycopg2
from psycopg2.sql import SQL, Identifier
from psycopg2.extras import execute_values
from helper_functions import read_config
import json


def read_db_connection():
    return {
        "host": read_config("secrets.cfg", "database", "host"),
        "user": read_config("secrets.cfg", "database", "user"),
        "password": read_config("secrets.cfg", "database", "password"),
        "dbname": read_config("secrets.cfg", "database", "dbname"),
        "port": read_config("secrets.cfg", "database", "port"),
    }


def get_sql_from_script(filepath: str):
    with open(filepath, 'r') as script:
        sql = script.read()
    return sql


def create_schema(schemaName: str):
    sql = get_sql_from_script("./scripts/sql/create_schema.sql")
    with psycopg2.connect(**read_db_connection()) as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(SQL(sql).format(Identifier(schemaName)))
        except Exception as e:
            # Rollback changes if exception
            conn.rollback()
            raise e
        finally:
            # Commit changes to the database
            conn.commit()

    # Close the connection - context manager won't do this for psycopg2
    conn.close()


def execute_query(sql_filepath: str, vars=None):
    sql = get_sql_from_script(sql_filepath)
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


def main(data_to_load: dict):
    """Loads API data into Postgres database.
    Parameters:
        data: The data to be loaded into the database
    """
    # Create the landing table if it doesn't exist
    create_schema("import")
    execute_query("./scripts/sql/create_table_playlist_snapshot.sql")

    # Insert the data into the landing table
    execute_query("./scripts/sql/insert_into_playlist_snapshot.sql", (json.dumps(data_to_load), ))


if __name__ == "__main__":
    dummy_extract = {
        "items": [
            {
                "track": {
                    "album": {
                        "id": "1bdKI997loh6G68NED2cwX",
                        "name": "Escapism. (Sped Up)",
                        "release_date": "2022-11-25",
                        "total_tracks": 2
                    },
                    "artists": [
                        {
                            "id": "5KKpBU5eC2tJDzf0wmlRp2",
                            "name": "RAYE"
                        },
                        {
                            "id": "12Zk1DFhCbHY6v3xep2ZjI",
                            "name": "070 Shake"
                        }
                    ],
                    "duration_ms": 272373,
                    "id": "5WxVXxCMRnvxUKFq40ELwq",
                    "name": "Escapism.",
                    "popularity": 79
                }
            },
            {
                "track": {
                    "album": {
                        "id": "1nrVofqDRs7cpWXJ49qTnP",
                        "name": "SOS",
                        "release_date": "2022-12-08",
                        "total_tracks": 23
                    },
                    "artists": [
                        {
                            "id": "7tYKF4w9nC0nq9CsPZTHyP",
                            "name": "SZA"
                        }
                    ],
                    "duration_ms": 153946,
                    "id": "1Qrg8KqiBpW07V7PNxwwwL",
                    "name": "Kill Bill",
                    "popularity": 90
                }
            },
        ]
    }
    main(dummy_extract)
