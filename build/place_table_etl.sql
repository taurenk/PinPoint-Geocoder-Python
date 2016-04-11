
DROP TABLE place_temp;
DROP TABLE place;

CREATE TABLE place_temp (iso_code varchar,
                        zip varchar,
                        place varchar,
                        name1 varchar,
                        code1 varchar,
                        name2 varchar,
                        code2 varchar,
                        name3 varchar,
                        code3 varchar,
                        latitude float,
                        longitude float,
                    	 accuracy varchar
                    );

\COPY place_temp FROM 'US.txt';

CREATE TABLE place ( id serial primary key,
			iso_code varchar,
                        zip varchar,
                        place varchar,
                        place_metaphone varchar(5),
                        state varchar,
                        state_metaphone varchar(5),
                        state_code varchar,
                        county varchar,
                        county_code varchar,
                        name3 varchar,
                        code3 varchar,
                        latitude float,
                        longitude float,
                    	 accuracy varchar
                    );

INSERT INTO place  (iso_code,
                        zip,
                        place,
                        place_metaphone,
                        state,
                        state_metaphone,
                        state_code,
                        county,
                        county_code,
                        name3,
                        code3,
                        latitude,
                        longitude,
                    	 accuracy) SELECT iso_code, zip, place, dmetaphone(place, 5), name1, dmetaphone(name1, 5), code1,
				name2,code2,name3,code3,latitude, longitude,accuracy
			FROM place_temp;
