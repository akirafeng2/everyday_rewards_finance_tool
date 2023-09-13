CREATE SCHEMA household;

CREATE TABLE household.weightings(
    item VARCHAR(50) PRIMARY KEY,
    adam FLOAT,
    alex FLOAT,
    tyler FLOAT,
    persist BOOLEAN DEFAULT FALSE
);

CREATE TABLE household.items_bought(
    id SERIAL PRIMARY KEY,
    item VARCHAR(50),
    price NUMERIC(7,2),
    payer VARCHAR(10)
);