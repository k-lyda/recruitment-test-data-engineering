#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy
import pandas as pd


def ingest_people_csv(db_conn):
    print("Loading People data...")
    people_df = pd.read_csv("/data/people.csv", sep=",", encoding="utf-8")
    print(f"Found {len(people_df)} records in csv file.")
    validate_people_df(people_df)

    people_df = map_places_to_ids(db_conn, people_df)
    load_df_to_database(db_conn, people_df, "person")


def ingest_places_csv(db_conn):
    print("Loading Places data...")
    places_df = pd.read_csv("/data/places.csv", sep=",", encoding="utf-8")
    print(f"Found {len(places_df)} records in csv file.")
    validate_places_data(places_df)

    load_df_to_database(db_conn, places_df, "place")


def validate_places_data(places_df):
    validate_no_of_columns(places_df, expected_columns_count=3)


def validate_people_df(people_df):
    validate_no_of_columns(people_df, expected_columns_count=4)


def validate_no_of_columns(df, expected_columns_count):
    no_of_columns = len(df.columns)
    if no_of_columns != expected_columns_count:
        raise ValueError(
            f"Places CSV has wrong number of columns. Has {no_of_columns}, should be {expected_columns_count}"
        )


def load_df_to_database(db_conn, df, table_name):
    print(f"Loading to: {table_name}.")
    print(f"Data to load: {df}")
    df.to_sql(
        table_name, db_conn, if_exists="append", method=None, index=False, chunksize=1
    )


def map_places_to_ids(db_conn, people_df):
    places_table = pd.read_sql("place", db_conn, columns=["id", "city"])
    people_df["place_of_birth_id"] = people_df["place_of_birth"].map(
        places_table.set_index("city")["id"]
    )
    people_df = people_df.drop(columns="place_of_birth")
    return people_df


def get_db_connection():
    # connect to the database
    engine = sqlalchemy.create_engine(
        "mysql://codetest:swordfish@database/codetest?charset=utf8mb4", encoding="utf-8"
    )
    connection = engine.connect()
    return connection


if __name__ == "__main__":
    with get_db_connection() as db_connection:
        ingest_places_csv(db_connection)
        ingest_people_csv(db_connection)
