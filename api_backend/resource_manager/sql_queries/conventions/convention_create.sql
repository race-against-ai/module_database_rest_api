INSERT INTO drivers
(name) 
VALUES (%s) 
RETURNING uuid;
