#PinPoint Geocoder 

[![Build Status](https://travis-ci.org/taurenk/PinPoint-Geocoder-Python.svg?branch=master)](https://travis-ci.org/taurenk/PinPoint-Geocoder-Python)
[![Coverage Status](https://coveralls.io/repos/github/taurenk/PinPoint-Geocoder-Python/badge.svg?branch=master)](https://coveralls.io/github/taurenk/PinPoint-Geocoder-Python?branch=master)

PinPoint is an Open Source Geocoding toolkit based off of TIGER/LINE and geonames.org data.
If you have any questions please feel free to contact me at tauren.kristich@gmail.com

### Setup and Database
**Database**
The application relies on a PostgreSQL database. I will have the official loading scripts up shortly. Please contact me if you 
would like access to my development database. 

**Environment Variables**
DB_NAME 
DB_USERNAME
DB_URL
DB_PASSWORD

### API
We currently have 2 Endpoints. In the future we hope to have an API into the US Census data tables and a reverse geocoder. 

**Geocoding API** 
/api/v1.0/geocoder/<address_string>

**Places API** 
/api/v1.0/place/<string:city>
Pulls city data from the place table provided by Geonames.org

**Address Features API(development)**
/api/v1.0/addressfeatures/<string:street_fullname>
Pulls street level data from US Census AddrFeat table



