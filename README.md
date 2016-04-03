#PinPoint Geocoder 

[![Build Status](https://circleci.com/gh/taurenk/PinPoint-Geocoder-Python.svg?style=shield&circle-token=1885263aee8c8d93993b8e7dc8d8a3f53a02a6f7)]

PinPoint is an Open Source Geocoding toolkit based off of TIGER/LINE and geonames.org data.
If you have any questions please feel free to contact me at tauren.kristich@gmail.com

### Setup and Database
The application relies on a PostgreSQL database. I will have the official loading scripts up shortly.

### API
We currently have 2 Endpoints. In the future we hope to have an API into the US Census data tables and a reverse geocoder. 

**Geocoding API** 
/api/v1.0/geocoder/<address_string>

**Places API** 
/api/v1.0/place/<string:city>
Pulls city data from the place table provided by Geonames.org


