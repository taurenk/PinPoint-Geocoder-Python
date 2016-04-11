#!/usr/bin/env bash
echo "*** PinPoint Database Loader ***"

psql_username="tauren"
psql_db="PinpointDB"
set PGPASSWORD="1elmstreet"

# Create Directories
mkdir build
mkdir build/staging
mkdir build/unzipped
"""
# Download Census Data
echo "Downloading Test Data for New York.. Please be Patient..."
lftp ftp2.census.gov << EOF
mirror -I "tl_2013_36*" /geo/tiger/TIGER2013/ADDRFEAT/ build/staging
quit 0
EOF

# Unzip Census Data
echo "Unzipping Data..."
count=0
for i in build/staging/*.zip; do
	unzip $i -d build/unzipped/
	count=$((count+1))
done
echo "Unzipped $count records."
"""

echo "Creating Table in Database..."
shp2pgsql -p build/unzipped/tl_2013_36001_addrfeat.shp addrfeat_staging | psql --host=pinpointdb.csxsl6g3bmig.us-east-1.rds.amazonaws.com \
                                                                               --port=5432 \
                                                                               --username=$psql_username \
                                                                               --dbname=$psql_db


# Load Records into Database
echo "Loading Database..."
for file in build/unzipped/*addrfeat.shp; do
	shp2pgsql -a $file addrfeat_staging | psql --host=pinpointdb.csxsl6g3bmig.us-east-1.rds.amazonaws.com \
                                               --port=5432 \
                                               --username=$psql_username \
                                               --dbname=$psql_db
done

# Load Place records
echo "Downloading and Loading Place Records..."
wget download.geonames.org/export/zip/US.zip
unzip US.zip
psql --host=pinpointdb.csxsl6g3bmig.us-east-1.rds.amazonaws.com \
                                               --port=5432 \
                                               --username=$psql_username \
                                               --dbname=$psql_db
                                               -f place_table_etl.sql
echo "Finished loading place data."
