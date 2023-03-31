#!/usr/bin/python
# encoding: utf-8
##############################################################################
#     dbInitialize.py - Build a new database
#
##############################################################################
# Copyright (c) 2023, 2024 Chad Sobodash
# All rights reserved.
# Licensed under the New BSD License
# (http://www.freebsd.org/copyright/freebsd-license.html)
##############################################################################

import sqlite3
from sqlite3 import Error
import os


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "optidrome.db"
    
    sql_create_user_table = """
        CREATE TABLE IF NOT EXISTS optidrome.user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    ); """

    sql_create_patient_table = """
        CREATE TABLE IF NOT EXISTS optidrome.patient (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        dob TEXT NOT NULL,
        phone TEXT NOT NULL CHECK (length(phone) = 12),
        street_address TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        zip TEXT NOT NULL CHECK (length(zip) = 5)
    ); """

    sql_create_rxorder_table = """
        CREATE TABLE IF NOT EXISTS optidrome.rxorder (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        frame_id INTEGER NOT NULL,
        lens_type TEXT NOT NULL,
        lens_material TEXT NOT NULL,
        lens_coating TEXT,
        pd REAL NOT NULL,
        origin_lab TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
        FOREIGN KEY (frame_id) REFERENCES frame(frame_id),
        FOREIGN KEY (origin_lab) REFERENCES lab(lab_name)
    ); """

    sql_create_frame_table = """
        CREATE TABLE IF NOT EXISTS optidrome.frame (
        frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
        frame_brand TEXT NOT NULL,
        frame_model TEXT NOT NULL,
        frame_color TEXT NOT NULL,
        frame_material TEXT NOT NULL,
        frame_shape TEXT NOT NULL,
        frame_style TEXT NOT NULL
    ); """

    sql_create_lens_table = """
        CREATE TABLE IF NOT EXISTS optidrome.lens (
        lens_id INTEGER PRIMARY KEY AUTOINCREMENT,
        lens_type TEXT NOT NULL,
        lens_material TEXT NOT NULL,
        lens_coating TEXT NOT NULL
    ); """

    sql_create_lab_table = """
        CREATE TABLE IF NOT EXISTS optidrome.lab (
        lab_id INTEGER PRIMARY KEY AUTOINCREMENT,
        lab_name TEXT NOT NULL,
        lab_address TEXT NOT NULL,
        lab_phone TEXT NOT NULL CHECK (length(phone) = 12),
        lab_fax TEXT NOT NULL CHECK (length(phone) = 12),
        lab_email TEXT NOT NULL UNIQUE,
    ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_patient_table)
        create_table(conn, sql_create_rxorder_table)
        create_table(conn, sql_create_frame_table)
        create_table(conn, sql_create_lens_table)
        create_table(conn, sql_create_lab_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()