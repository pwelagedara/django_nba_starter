#!/bin/bash

##############################################################################
##
##  Project initialization script for Django NBA starter
##
##############################################################################

GREEN=$'\e[1;32m'
DEFAULT=$'\e[0m'

echo $GREEN
cat << EOF
+-+-+-+-+-+-+ +-+-+-+ +-+-+-+-+-+-+-+
|D|j|a|n|g|o| |N|B|A| |S|t|a|r|t|e|r|
+-+-+-+-+-+-+ +-+-+-+ +-+-+-+-+-+-+-+
EOF
echo $DEFAULT

# Delete database
echo $GREEN[INFO] Deleting database$DEFAULT
rm -f db.sqlite3

# Migrations
echo $GREEN[INFO] Migrations$DEFAULT
./migrate.sh

# Create super user
echo $GREEN[INFO] Creating super user$DEFAULT
./createsuperuser.sh

sleep 2

# Initialize data
echo $GREEN[INFO] Populating data$DEFAULT
./initializedata.sh

echo $GREEN[INFO] Completed$DEFAULT
