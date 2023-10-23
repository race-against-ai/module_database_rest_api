-- SQL Query for Creating the Database and Tables --
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    createdAt TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE TABLE conventions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    date DATE
);

CREATE TABLE drivertimes (
    id SERIAL PRIMARY KEY,
    sector1 FLOAT NOT NULL,
    sector2 FLOAT NOT NULL,
    sector3 FLOAT NOT NULL,
    laptime FLOAT NOT NULL,
    driver UUID REFERENCES drivers(id),
    convention INTEGER REFERENCES conventions(id)
);



