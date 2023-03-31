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
import os
print(os.getcwd())

# Creates tables user, patient, rxorder, frame, and lens.

conn = sqlite3.connect('optidrome.db')
c = conn.cursor()

c.execute('''
            CREATE TABLE IF NOT EXISTS optidrome.user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
)''')

c.execute('''
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
)''')

c.execute('''
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
)''')

c.execute('''
            CREATE TABLE IF NOT EXISTS optidrome.frame (
            frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
            frame_brand TEXT NOT NULL,
            frame_model TEXT NOT NULL,
            frame_color TEXT NOT NULL,
            frame_material TEXT NOT NULL,
            frame_shape TEXT NOT NULL,
            frame_style TEXT NOT NULL
)''')

c.execute('''
            CREATE TABLE IF NOT EXISTS optidrome.lens (
            lens_id INTEGER PRIMARY KEY AUTOINCREMENT,
            lens_type TEXT NOT NULL,
            lens_material TEXT NOT NULL,
            lens_coating TEXT NOT NULL
)''')

c.execute('''
            CREATE TABLE IF NOT EXISTS optidrome.lab (
            lab_id INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_name TEXT NOT NULL,
            lab_address TEXT NOT NULL,
            lab_phone TEXT NOT NULL CHECK (length(phone) = 12),
            lab_fax TEXT NOT NULL CHECK (length(phone) = 12),
            lab_email TEXT NOT NULL UNIQUE,
)''')

conn.commit()
conn.close()
