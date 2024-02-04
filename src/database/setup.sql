-- Check the environment variable 'ENV'
DO $$
DECLARE
    schema_name text;
BEGIN
    -- Get the schema name from the environment variable
    schema_name := current_setting('ENV', true);
    
    -- Create the schema if it doesn't exist
    EXECUTE 'CREATE SCHEMA IF NOT EXISTS ' || schema_name;
    
    -- Set the search_path to the specified schema
    EXECUTE 'SET search_path TO ' || schema_name;
END $$;

-- Create function
CREATE OR REPLACE FUNCTION generate_household_password()
RETURNS TEXT AS $$
DECLARE
    result TEXT;
BEGIN
    result := substr(md5(random()::text), 1, 8);
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Create your tables here
CREATE TABLE household (
  household_id SERIAL PRIMARY KEY,
  household_name VARCHAR(50) NOT NULL UNIQUE,
  household_password VARCHAR(8) NOT NULL UNIQUE
);

CREATE TABLE item (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE profile (
    profile_id character(36) PRIMARY KEY,
    household_id INT, 
    user_name VARCHAR(12) NOT NULL, -- removed UNIQUE
    -- email VARCHAR(320) NOT NULL UNIQUE, --new
    -- password_hash VARCHAR(32) NOT NULL, --new
    FOREIGN KEY (household_id) REFERENCES household(household_id)
);

CREATE TABLE receipt (
    receipt_id SERIAL PRIMARY KEY,
    receipt_date DATE NOT NULL,
    profile_id character(36) NOT NULL, 
    source VARCHAR(20) CHECK (source IN ('receipt', 'one_off', 'recurring', 'weighting_update')),
    FOREIGN KEY (profile_id) REFERENCES profile(profile_id)
);

CREATE TABLE weighting (
    weighting_id INT NOT NULL,
    profile_id character(36) NOT NULL,
    weighting NUMERIC(7,2) CHECK (weighting IS NOT NULL AND weighting >= 0),
    PRIMARY KEY (weighting_id, profile_id),
    FOREIGN KEY (profile_id) REFERENCES profile(profile_id)
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    item_id INT NOT NULL,
    receipt_id INT NOT NULL,
    price NUMERIC(7,2) CHECK (price IS NOT NULL AND price >= 0),
    weighting_id INT,
    weighting_persist BOOLEAN DEFAULT FALSE,
    active_ind BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (item_id) REFERENCES item(item_id),
    FOREIGN KEY (receipt_id) REFERENCES receipt(receipt_id)
);
-- -- Additional table creations go here...


-- ---
-- CREATE SCHEMA household;

-- CREATE TABLE household.weightings(
--     item VARCHAR(50) PRIMARY KEY,
--     adam FLOAT,
--     alex FLOAT,
--     tyler FLOAT,
--     persist BOOLEAN DEFAULT FALSE
-- );

-- CREATE TABLE household.items_bought(
--     id SERIAL PRIMARY KEY,
--     item VARCHAR(50),
--     price NUMERIC(7,2),
--     payer VARCHAR(10)
-- );

-- CREATE VIEW household.items_and_weightings AS
-- SELECT a.id as id, a.item as item, a.price as price, a.payer as payer, b.adam as adam, b.alex as alex, b.tyler as tyler, b.persist as persist
-- FROM household.items_bought as a
-- LEFT JOIN household.weightings as b on a.item = b.item;

-- CREATE TABLE household.one_off_expenses(
--     id SERIAL PRIMARY KEY,
--     item VARCHAR(50),
--     price NUMERIC(7,2),
--     payer VARCHAR(10),
--     adam FLOAT,
--     alex FLOAT,
--     tyler FLOAT
-- );

-- CREATE TABLE household.recurring_expenses(
--     id SERIAL PRIMARY KEY,
--     item VARCHAR(50),
--     price NUMERIC(7,2),
--     payer VARCHAR(10),
--     adam FLOAT,
--     alex FLOAT,
--     tyler FLOAT
-- );

-- CREATE VIEW household.combined_expenses AS
-- SELECT item, price, payer, adam, alex, tyler FROM household.items_and_weightings
-- UNION ALL 
-- SELECT item, price, payer, adam, alex, tyler FROM household.one_off_expenses
-- UNION ALL 
-- SELECT item, price, payer, adam, alex, tyler FROM household.recurring_expenses;


-- ---
-- \set environment value
-- CREATE TABLE dev.transactions