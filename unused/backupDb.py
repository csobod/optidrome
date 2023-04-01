#!/usr/bin/python
# encoding: utf-8
##############################################################################
#     dbBackup.py - Database backup screen 
#
##############################################################################
# Copyright (c) 2022, 2023 David Villena
# All rights reserved.
# Licensed under the New BSD License
# (http://www.freebsd.org/copyright/freebsd-license.html)
##############################################################################

import curses
import npyscreen
from npyscreen import wgwidget as widget
import config
import bsWidgets as bs
import sqlite3
from sqlite3 import Error
import os.path

TAB = "\t"
CR = "\n"

helpText = "\nThis is a module to backup the database. It will create a backup file with \n" +\
    "the extension .bak in the same folder as the database file.\n\n" +\
    "If the database file is not found, it will create a new database file.\n"


class DbBackupForm(npyscreen.FormBaseNew):
    "Form to backup database."
    def __init__(self, name="DbBackup", parentApp=None, framed=None, help=None, color='FORMDEFAULT',\
    widget_list=None, cycle_widgets=False, ok_button_function=None, cancel_button_function=None, *args, **keywords):

        """ Create the parent, npyscreen._FormBase """
        super().__init__(name, parentApp, framed, help, color, widget_list, cycle_widgets=cycle_widgets, *args, **keywords)

    def create(self):
        """The standard constructor will call the method .create(), which you should override to create the Form widgets."""
        self.framed = True # Framed form
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.exitDbBackup # Escape exit

        # Form title
        pname, version = config.pname, config.program_version
        self.formTitle = pname + " " + version + " - Database backup"
        self.title = self.add(bs.MyFixedText, name="DbBackup", value=self.formTitle,\
            relx=2, rely=0, editable=False) # Screen title line
        #-------------------------------------------------------------------------------------------------------------------------
        self.infoTxt = self.add(bs.MyMultiLineEdit, name="", value="", relx=13, rely=6, max_height=3, editable=False)
        info = "Warning: this will delete the current backup,\n" +\
               "and create a new backup of the current database."
        self.infoTxt.value = info
        #-------------------------------------------------------------------------------------------------------------------------
        self.ok_button=self.add(Mi_MiniButtonPress, name="Delete records", relx=21, rely=19, editable=True)
        self.ok_button.when_pressed_function = self.DbBackupbtn_function
        self.cancel_button=self.add(Mi_MiniButtonPress, name="Cancel", relx=45, rely=19, editable=True)
        self.cancel_button.when_pressed_function = self.Cancelbtn_function

    def DbBackupbtn_function(self):
        "Check Database button function."
        self.backupDb()

    def Cancelbtn_function(self):
        "Cancel button function."
        self.exitDbBackup()

    def exitDbBackup(self):
        config.parentApp.setNextForm("DBMANAGER")
        config.parentApp.switchFormNow()

    def backupDb(self):
        """Backup database."""
        dbBackupPath = dataPath + dbname + ".bak"
        dbCurrentPath = dataPath + dbname
        checkBackup = os.path.isfile(dbBackupPath)

        if print(checkBackup) == True:  # Old database backup file exists
            os.remove(dbBackupPath) # Delete old backup file
            if system == "Windows":
                os.popen("copy " + dbCurrentPath + " " + dbBackupPath)
            elif system == "Linux":
                os.popen("cp " + dbCurrentPath + " " + dbBackupPath)
        else:   # No database backup file exists
            if system == "Windows":
                os.popen("copy " + dbCurrentPath + " " + dbBackupPath)
            elif system == "Linux":
                os.popen("cp " + dbCurrentPath + " " + dbBackupPath)

#def initialize_database():
    # Create new database
#    print("Creating new database...")
#    create_connection(../Data/Optidrome.db)

#def create_connection(db_file):
#    """ create a database connection to a SQLite database """
#    conn = None
#    try:
#        conn = sqlite3.connect(db_file)
#        print(sqlite3.version)
#    except Error as e:
#        print(e)
#    finally:
#        if conn:
#            conn.close()

#def create_table(conn, create_table_sql):
#    """ create a table from the create_table_sql statement
#    :param conn: Connection object
#    :param create_table_sql: a CREATE TABLE statement
#    :return:
#    """
#    try:
#        c = conn.cursor()
#        c.execute(create_table_sql)
#    except Error as e:
#        print(e)