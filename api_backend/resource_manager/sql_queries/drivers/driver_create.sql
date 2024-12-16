INSERT INTO drivers
(name) 
VALUES (%s) 
RETURNING id;
