\c finance_db;

CREATE SCHEMA household;

CREATE TABLE household.weightings(
    item VARCHAR(50) PRIMARY KEY,
    adam FLOAT,
    alex FLOAT,
    tyler FLOAT,
    persist BOOLEAN DEFAULT TRUE
);

CREATE TABLE household.items_bought(
    item VARCHAR(50),
    price NUMERIC(7,2),
    payer VARCHAR(10)
);