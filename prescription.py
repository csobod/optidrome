#!/usr/bin/python
# encoding: utf-8
##############################################################################
#     prescription.py - Create a new prescription
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

DATEFORMAT = config.dateFormat
DBTABLENAME = "'optidrome.prescription'"

global format

helpText = "Stores patient prescriptions.\n\n" \
            "Prescriptions are stored in a database table and can be added " \
            "and removed from the database.  The database is encrypted " \
            "using a password that is stored in the configuration file.  "

class PrescriptionForm(npyscreen.FormBaseNew):
    "Prescription entry form called by patient form."
    def __init__(self, name="Prescription", parentApp=None, framed=None, help=None, color='FORMDEFAULT',\
        widget_list=None, cycle_widgets=False, ok_button_function=None, cancel_button_function=None, *args, **keywords):

        # Creates the parent, npyscreen.FormBaseNew.
        super().__init__(name, parentApp, framed, help, color, widget_list, cycle_widgets=cycle_widgets, *args, **keywords)

        global form
        form = self

        self.selectorForm = self.parentApp._Forms['PATIENT']

    def create(self):
        """The standard constuctor will call the method .create(), which you should override to create your widgets."""
        self.framed = True  # framed form
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_prescription  # Escape exit

        # Form title
        pname, version = config.pname, config.program_version
        self.formTitle = pname + " " + version + " - Prescription"
        self.formTitleFld = self.add(bs.MyFixedText, name="PrescriptionTitle", value=self.formTitle, relx=2, rely=0, editable=False)    # Screen title line

        # Form fields
        