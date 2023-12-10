CREATE EXTENSION IF NOT EXISTS dblink;

------ Добавление информации в таблицы ------

-- Добавление данных аккаунта пользователя в таблицу account
DROP FUNCTION IF EXISTS insert_account(VARCHAR(15), VARCHAR(20));
CREATE OR REPLACE FUNCTION insert_account(user_name VARCHAR(15), pass_word VARCHAR(20))
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO account (username, password) VALUES (user_name, pass_word);
    END;
    $$
LANGUAGE plpgsql;

-- Добавление информации о пользователе в таблицу user_info
DROP FUNCTION IF EXISTS insert_user_info(character varying, integer, numeric, numeric, character varying, integer, text);
CREATE OR REPLACE FUNCTION insert_user_info(
    user_gender VARCHAR(6),
    user_age INT,
    user_weight NUMERIC,
    user_height NUMERIC,
    user_activity VARCHAR(10),
    user_account_id INT,
    user_goal TEXT
)
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO user_info (gender, activity, age, weight, height, goal, account_id)
        VALUES (user_gender, user_activity, user_age, user_weight, user_height, user_goal, user_account_id);
    END;
    $$
LANGUAGE plpgsql;

-- Вставка информации об приеме пищи --
DROP FUNCTION IF EXISTS insert_meal_info(VARCHAR(10), DATE, NUMERIC, NUMERIC, NUMERIC, NUMERIC, INT);
CREATE OR REPLACE FUNCTION insert_meal_info(
    curr_meal_type VARCHAR(10),
    curr_date DATE,
    curr_proteins NUMERIC,
    curr_fats NUMERIC,
    curr_carbohydrates NUMERIC,
    curr_kilocalories NUMERIC,
    curr_user_id INT
)
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO meal (meal_type, date, proteins, fats, carbohydrates, kilocalories, user_id)
        VALUES (curr_meal_type, curr_date, curr_proteins, curr_fats, curr_carbohydrates, curr_kilocalories, curr_user_id);
    END;
    $$
LANGUAGE plpgsql;

-- Добавление данных об продуктах в БД --
DROP FUNCTION IF EXISTS insert_product_info(INTEGER, TEXT, NUMERIC, NUMERIC, NUMERIC, NUMERIC);
CREATE OR REPLACE FUNCTION insert_product_info(
    curr_id INTEGER,
    curr_name TEXT,
    curr_proteins NUMERIC,
    curr_fats NUMERIC,
    curr_carbohydrates NUMERIC,
    curr_kilocalories NUMERIC
)
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO product (id, name, proteins, fats, carbohydrates, kilocalories)
        VALUES (curr_id, curr_name, curr_proteins, curr_fats, curr_carbohydrates, curr_kilocalories);
    END;
    $$
LANGUAGE plpgsql;

-- Добавление продукта в категорию избранное --
DROP FUNCTION IF EXISTS add_product_to_favourites(INTEGER, INTEGER);
CREATE OR REPLACE FUNCTION add_product_to_favourites(
    curr_user_id INTEGER,
    curr_product_id INTEGER
)
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO favourites (user_id, product_id)
        VALUES (curr_user_id, curr_product_id);
    END;
    $$
LANGUAGE plpgsql;

-- Добавление статистики пользователя за сутки --
DROP FUNCTION IF EXISTS add_statistic_info(numeric, numeric, numeric, numeric, DATE, numeric, INTEGER);
CREATE OR REPLACE FUNCTION add_statistic_info(
    curr_kilocalories numeric,
    curr_fats numeric,
    curr_carbohydrates numeric,
    curr_proteins numeric,
    curr_date DATE,
    curr_weight_loss numeric,
    curr_user_id INTEGER

)
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO user_statistic (kilocalories_intake, fats_intake, carbohydrates_intake, proteins_intake, date, weight_loss, user_id)
        VALUES (curr_kilocalories, curr_fats, curr_carbohydrates, curr_proteins, curr_date, curr_weight_loss, curr_user_id);
    END;
    $$
LANGUAGE plpgsql;

