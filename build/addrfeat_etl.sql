/*
Tauren Kristich
Edit the addrfeat stating in place, and rename it (cutting down on time for now).
*/

ALTER TABLE addrfeat_staging
	ADD fullname_metaphone VARCHAR(10);

UPDATE addrfeat_staging
	SET fullname_metaphone = dmetaphone(fullname);

DROP TABLE addrfeat;
ALTER TABLE addrfeat_staging
	RENAME TO addrfeat;


CREATE INDEX ON addrfeat (zipl);
CREATE INDEX ON addrfeat (zipr);
CREATE INDEX ON addrfeat (fullname_metaphone);