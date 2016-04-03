#PinPoint Geocoder 

https://circleci.com/gh/:owner/:repo.svg?style=shield&circle-token=:circle-token

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


