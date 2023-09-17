CREATE SCHEMA household;

CREATE TABLE household.weightings(
    item VARCHAR(50) PRIMARY KEY,
    adam FLOAT,
    alex FLOAT,
    tyler FLOAT,
    persist BOOLEAN DEFAULT TRUE
);

CREATE TABLE household.items_bought(
    id SERIAL PRIMARY KEY,
    item VARCHAR(50),
    price NUMERIC(7,2),
    payer VARCHAR(10)
);

CREATE VIEW household.items_and_weightings AS
SELECT a.id as id, a.item as item, a.price as price, a.payer as payer, b.adam as adam, b.alex as alex, b.tyler as tyler, b.persist as persist
FROM household.items_bought as a
LEFT JOIN household.weightings as b on a.item = b.item;