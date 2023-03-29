#!/usr/bin/python
# encoding: utf-8
##############################################################################
#     mainMenu.py - Main menu screen
#
##############################################################################
# Copyright (c) 2022, 2023 David Villena
#               2023, 2024 Chad Sobodash
# All rights reserved.
# Licensed under the New BSD License
# (http://www.freebsd.org/copyright/freebsd-license.html)
##############################################################################

import sqlite3
import os
print(os.getcwd())


conn = sqlite3.connect('eyeglass_store.db')
c = conn.cursor()

c.execute('''
            CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
)''')

c.execute('''
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
            zip TEXT NOT NULL CHECK (length(zip) = 5)
)''')

c.execute('''
            CREATE TABLE IF NOT EXISTS rxorder (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            frame_id INTEGER NOT NULL,
            lens_type TEXT NOT NULL,
            lens_material TEXT NOT NULL,
            lens_coating TEXT,
            pd REAL NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
            FOREIGN KEY (frame_id) REFERENCES frame(frame_id)
)''')

c.execute('''
            CREATE TABLE IF NOT EXISTS frame (
            frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
            frame_brand TEXT NOT NULL,
            frame_model TEXT NOT NULL,
            frame_color TEXT NOT NULL,
            frame_material TEXT NOT NULL,
            frame_shape TEXT NOT NULL,
            frame_style TEXT NOT NULL
)''')

c.execute('''
            CREATE TABLE IF NOT EXISTS lens (
            lens_id INTEGER PRIMARY KEY AUTOINCREMENT,
            lens_type TEXT NOT NULL,
            lens_material TEXT NOT NULL,
            lens_coating TEXT NOT NULL
)''')

conn.commit()
conn.close()
