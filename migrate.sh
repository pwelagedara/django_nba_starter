#!/bin/bash

##############################################################################
##
##  Migration script for Django NBA starter
##
##############################################################################

# Make migrations
python manage.py makemigrations

# Migrate
python manage.py migrate