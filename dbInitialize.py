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

import datetime
import sqlite3
from sqlite3 import Error
import time

import base64

import bsWidgets as bs
import config

DATEFORMAT = "%Y-%m-%d %H:%M:%S"
db_file = config.dataPath + config.dbname


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
        raw_password = '1234'
        password = base64.b64encode(raw_password.encode('utf-8')).decode('utf-8')
        numeral = 1
        user_name = 'Admin'
        user = 'admin'
        user_level = 1
        creation_date = datetime.datetime.now().strftime(DATEFORMAT)
        user_data = [(numeral, user, user_name, user_level, creation_date, password)]
        c = conn.cursor()
        c.executemany('INSERT INTO "optidrome.user" (numeral,user,user_name,user_level,creation_date,password) VALUES (?,?,?,?,?,?) ', user_data)
        conn.commit()
    except Error as e:
        print(e)


def main():

    sql_create_user_table = """
    CREATE TABLE "optidrome.user" (
        "id"	INTEGER NOT NULL UNIQUE,
        "numeral"	INTEGER NOT NULL UNIQUE,
        "user"	TEXT NOT NULL UNIQUE,
        "user_name"	TEXT,
        "user_level"	INTEGER NOT NULL,
        "creation_date"	TEXT NOT NULL,
        "password"	TEXT NOT NULL,
        PRIMARY KEY("id")
    ); """

    sql_create_patient_table = """
    CREATE TABLE IF NOT EXISTS "optidrome.patient" (
        "id"    INTEGER NOT NULL UNIQUE,
        "mrn"   INTEGER NOT NULL UNIQUE,
        "name"  TEXT NOT NULL,
        "dob"   TEXT NOT NULL,
        "phone" TEXT NOT NULL CHECK (length(phone) >= 10),
        "email" TEXT NOT NULL UNIQUE,
        "address"   TEXT NOT NULL,
        PRIMARY KEY("id")
    ); """

    sql_create_vendor_table = """
    CREATE TABLE IF NOT EXISTS "optidrome.vendor" (
        "id" INTEGER NOT NULL UNIQUE,
        "vendor_num" INTEGER NOT NULL UNIQUE,
        "name" TEXT NOT NULL,
        "address" TEXT NOT NULL,
        "phone" TEXT NOT NULL CHECK (length("phone") = 12),
        "fax" TEXT NOT NULL CHECK (length("fax") = 12),
        "email" TEXT NOT NULL UNIQUE,
        "website" TEXT NOT NULL,
        "is_lab" BOOLEAN NOT NULL,
        PRIMARY KEY("id")
    ); """

    sql_create_frame_table = """
    CREATE TABLE IF NOT EXISTS "optidrome.frame" (
        "id" INTEGER NOT NULL UNIQUE,
        "sku" INTEGER NOT NULL UNIQUE,
        "vendor_id" INTEGER NOT NULL,
        "make" TEXT NOT NULL,
        "model" TEXT NOT NULL,
        "color" TEXT NOT NULL,
        "material" TEXT NOT NULL,
        "edge_type" TEXT NOT NULL,
        "a" REAL NOT NULL,
        "b" REAL NOT NULL,
        "ed" REAL NOT NULL,
        "dbl" REAL NOT NULL,
        "temple" REAL NOT NULL,
        "cost" REAL NOT NULL,
        "price" REAL NOT NULL,
        PRIMARY KEY("id"),
        FOREIGN KEY ("vendor_id") REFERENCES "optidrome.vendor"("vendor_num")
    ); """

    sql_create_lens_table = """
    CREATE TABLE IF NOT EXISTS "optidrome.lens" (
        "id" INTEGER NOT NULL UNIQUE,
        "sku" INTEGER NOT NULL UNIQUE,
        "type" TEXT NOT NULL,
        "design" TEXT NOT NULL,
        "material" TEXT NOT NULL,
        "origin_lab_num" INTEGER NOT NULL,
        "cost" REAL NOT NULL,
        "price" REAL NOT NULL,
        PRIMARY KEY("id"),
        FOREIGN KEY ("origin_lab_num") REFERENCES "optidrome.vendor"("vendor_num")
    ); """

    sql_create_rxorder_table = """
        CREATE TABLE IF NOT EXISTS "optidrome.rxorder" (
        "id" INTEGER NOT NULL UNIQUE,
        "job" INTEGER NOT NULL UNIQUE,
        "patient_mrn" INTEGER NOT NULL,
        "frame_id" INTEGER,
        "lens_id" INTEGER,
        "lens_color" TEXT NOT NULL,
        "tint_color_id" INTEGER,
        "tint_intensity" INTEGER,
        "treatment" TEXT,
        "edge_treatment" TEXT NOT NULL,
        "uncut" BOOLEAN NOT NULL,
        "coating_id" TEXT NOT NULL,
        "pd" REAL NOT NULL,
        "origin_lab" TEXT NOT NULL,
        "invoice" INTEGER,
        "creation_date"	TEXT NOT NULL,
        "order_status" INTEGER NOT NULL,
        "order_type" TEXT NOT NULL,
        "order_payment" TEXT NOT NULL,
        "order_paymentstatus" TEXT NOT NULL,
        "order_paymentdate" TEXT NOT NULL,
        "order_paymentamount" REAL NOT NULL,
        "order_paymentmethod" TEXT NOT NULL,
        "order_paymentnotes" TEXT,
        order_shipdate TEXT NOT NULL,
        order_shipmethod TEXT NOT NULL,
        order_shiptracking TEXT NOT NULL,
        order_shipnotes TEXT,
        "notes" TEXT,
        PRIMARY KEY("id"),
        FOREIGN KEY ("patient_mrn") REFERENCES "optidrome.patient"("mrn"),
        FOREIGN KEY ("frame_id") REFERENCES "optidrome.frame"("sku"),
        FOREIGN KEY ("lens_id") REFERENCES "optidrome.lens"("sku"),
        FOREIGN KEY ("origin_lab") REFERENCES "optidrome.lens"("origin_lab_num")
    ); """

    conn = create_connection(db_file)

    if conn is not None:
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_patient_table)
        create_table(conn, sql_create_vendor_table)
        create_table(conn, sql_create_frame_table)
        create_table(conn, sql_create_lens_table)
        create_table(conn, sql_create_rxorder_table)
        create_user(conn)
        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()