#!/usr/bin/env python

import sqlalchemy
import pandas as pd


def extract_summary_to_json(mysql_conn):
    query = "select country, count(*) as people_count from person inner join place on place.id = person.place_of_birth_id group by country"

    born_in_country_df = pd.read_sql_query(query, mysql_conn)

    path = "/data/summary_output.json"
    born_in_country_df.set_index("country")["people_count"].to_json(
        path, orient="index"
    )


def get_db_connection():
    # connect to the database
    engine = sqlalchemy.create_engine(
        "mysql://codetest:swordfish@database/codetes?charset=utf8mb4"
    )
    connection = engine.connect()
    return connection


if __name__ == "__main__":
    with get_db_connection() as db_connection:
        extract_summary_to_json(db_connection)
