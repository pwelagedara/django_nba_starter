#!/bin/bash

##############################################################################
##
##  Migration script for Django NBA starter
##
##############################################################################

# Make migrations
python manage.py makemigrations

# Make view migrations
python manage.py makeviewmigrations

# Migrate
python manage.py migrate