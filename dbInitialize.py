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
import platform
import base64

system = platform.system()
system_release = platform.release()
if system == "Windows":
    dataPath = os.getcwd().replace("\\", "/") + "/Data/"
elif system == "Linux":
    dataPath = os.getcwd() + "/Data/"

db_file = dataPath + "optidrome.db"


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
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


def create_user(conn):
    """
    Create a new user into the user table
    :param conn:
    :param user:
    :return: user id
    """
    try:
        password = '1234'
        encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
        user = 'Admin'
        user_login = 'admin'
        user_data = [(user, user_login, encoded_password)]
        c = conn.cursor()
        c.executemany('INSERT INTO user (user,username,password) VALUES (?,?,?) ', user_data)
        conn.commit()
    except Error as e:
        print(e)


def main():

    sql_create_user_table = """
        CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL UNIQUE,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    ); """

    sql_create_patient_table = """
        CREATE TABLE IF NOT EXISTS patient (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        dob TEXT NOT NULL,
        phone TEXT NOT NULL CHECK (length(phone) = 12),
        street_address TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        zip TEXT NOT NULL CHECK (length(zip) = 10)
    ); """

    sql_create_frame_table = """
        CREATE TABLE IF NOT EXISTS frame (
        frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
        frame_make TEXT NOT NULL,
        frame_model TEXT NOT NULL,
        frame_color TEXT NOT NULL,
        frame_material TEXT NOT NULL,
        frame_style TEXT NOT NULL,
        frame_cost REAL NOT NULL,
        frame_price REAL NOT NULL
    ); """

    sql_create_lens_table = """
        CREATE TABLE IF NOT EXISTS lens (
        lens_id INTEGER PRIMARY KEY AUTOINCREMENT,
        lens_type TEXT NOT NULL,
        lens_material TEXT NOT NULL,
        lens_coating TEXT NOT NULL,
        lens_cost REAL NOT NULL,
        lens_price REAL NOT NULL
    ); """

    sql_create_lab_table = """
        CREATE TABLE IF NOT EXISTS lab (
        lab_id INTEGER PRIMARY KEY AUTOINCREMENT,
        lab_name TEXT NOT NULL,
        lab_address TEXT NOT NULL,
        lab_phone TEXT NOT NULL CHECK (length(lab_phone) = 12),
        lab_fax TEXT NOT NULL CHECK (length(lab_fax) = 12),
        lab_email TEXT NOT NULL UNIQUE
    ); """

    sql_create_rxorder_table = """
        CREATE TABLE IF NOT EXISTS rxorder (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        frame_id INTEGER NOT NULL,
        lens_material TEXT NOT NULL,
        lens_style TEXT NOT NULL,
        lens_augment TEXT NOT NULL,
        lens_coat TEXT NOT NULL,
        pd REAL NOT NULL,
        origin_lab TEXT NOT NULL,
        invoice_number TEXT NOT NULL,
        order_date TEXT NOT NULL,
        order_status TEXT NOT NULL,
        order_type TEXT NOT NULL,
        order_payment TEXT NOT NULL,
        order_paymentstatus TEXT NOT NULL,
        order_paymentdate TEXT NOT NULL,
        order_paymentamount REAL NOT NULL,
        order_paymentmethod TEXT NOT NULL,
        order_paymentnotes TEXT,
        order_shipdate TEXT NOT NULL,
        order_shipmethod TEXT NOT NULL,
        order_shiptracking TEXT NOT NULL,
        order_shipnotes TEXT,
        order_notes TEXT,
        FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
        FOREIGN KEY (frame_id) REFERENCES frame(frame_id),
        FOREIGN KEY (origin_lab) REFERENCES lab(lab_name)
    ); """

    conn = create_connection(db_file)

    if conn is not None:
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_patient_table)
        create_table(conn, sql_create_rxorder_table)
        create_table(conn, sql_create_frame_table)
        create_table(conn, sql_create_lens_table)
        create_table(conn, sql_create_lab_table)
        create_user(conn)
        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()