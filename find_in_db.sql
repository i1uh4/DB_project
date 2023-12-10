------ Поиск содержимого таблиц ------

-- Поиск id из таблицы user_info
DROP FUNCTION IF EXISTS find_user_id(INT);
CREATE OR REPLACE FUNCTION find_user_id(acc_id INT)
    RETURNS INT AS
    $$
    DECLARE
        user_id_result INT;
    BEGIN
        SELECT id INTO user_id_result
        FROM user_info
        WHERE account_id = acc_id;

        RETURN user_id_result;
    END;
    $$
LANGUAGE plpgsql;


-- Поиск пароля пользователя для валидации
DROP FUNCTION IF EXISTS find_account_id_and_password(varchar(15));
CREATE OR REPLACE FUNCTION find_account_id_and_password(user_login varchar(15))
    RETURNS TABLE(id INTEGER, password VARCHAR) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT account.id, account.password
        FROM account
        WHERE account.username = user_login;
    END;
    $$
LANGUAGE plpgsql;


-- Поиск продуктов по названию --
DROP FUNCTION IF EXISTS find_product(VARCHAR(40));
CREATE OR REPLACE FUNCTION find_product(product_name VARCHAR(40))
    RETURNS TABLE (
        id INTEGER,
        name text,
        proteins NUMERIC,
        fats NUMERIC,
        carbohydrates NUMERIC,
        kilocalories NUMERIC
    ) AS
    $$
    BEGIN
        IF EXISTS (SELECT prod.name FROM product prod WHERE prod.name LIKE '%' || product_name || '%') THEN
			RETURN QUERY
            SELECT * FROM product WHERE product.name LIKE '%' || product_name || '%';
		ELSE
			RAISE NOTICE 'Client with name % does not exist', product_name;
		END IF;

    END;
    $$
LANGUAGE plpgsql;


-- Поиск конкретного продукта в категории избранное --
DROP FUNCTION IF EXISTS get_fav_product(INTEGER, INTEGER);
CREATE OR REPLACE FUNCTION get_fav_product(curr_user_id INTEGER, curr_prod_id INTEGER)
RETURNS INTEGER AS
$$
DECLARE
    favProductId INT;
BEGIN
    SELECT COALESCE(fav.product_id, NULL) INTO favProductId
    FROM favourites fav
    WHERE fav.user_id = curr_user_id AND fav.product_id = curr_prod_id
    LIMIT 1;

    RETURN favProductId;
END;
$$
LANGUAGE plpgsql;


-- Поиск информации о продукте --
DROP FUNCTION IF EXISTS get_product_info(INTEGER);
CREATE OR REPLACE FUNCTION get_product_info(product_id INTEGER)
    RETURNS TABLE (
        proteins NUMERIC,
        fats NUMERIC,
        carbohydrates NUMERIC,
        kilocalories NUMERIC
    ) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT prod.proteins, prod.fats, prod.carbohydrates, prod.kilocalories FROM product prod WHERE id = product_id;
    END;
    $$
LANGUAGE plpgsql;


-- Поиск информации о конкретном приеме пищи --
DROP FUNCTION IF EXISTS get_meal_info(varchar(10), date, INTEGER);
CREATE OR REPLACE FUNCTION get_meal_info(curr_meal_type varchar(10), curr_date date, curr_user_id INTEGER)
    RETURNS TABLE (
        proteins NUMERIC,
        fats NUMERIC,
        carbohydrates NUMERIC,
        kilocalories NUMERIC
    ) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT meal.proteins, meal.fats, meal.carbohydrates, meal.kilocalories FROM meal
        WHERE meal_type = curr_meal_type AND date = curr_date AND user_id = curr_user_id;
    END;
    $$
LANGUAGE plpgsql;


-- Поиск продуктов, которые добавлены в категорию избранных --
DROP FUNCTION IF EXISTS get_favourite_products(INTEGER);
CREATE OR REPLACE FUNCTION get_favourite_products(curr_user_id INTEGER)
    RETURNS TABLE (
        id INTEGER,
        name text,
        proteins NUMERIC,
        fats NUMERIC,
        carbohydrates NUMERIC,
        kilocalories NUMERIC
    ) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT prod.id, prod.name, prod.proteins, prod.fats, prod.carbohydrates, prod.kilocalories
        FROM product prod
        JOIN favourites fav ON prod.id = fav.product_id
        WHERE user_id = curr_user_id
        ORDER BY fav.id;
    END;
    $$
LANGUAGE plpgsql;


-- Поиск продуктов в тбалице product --
DROP FUNCTION IF EXISTS get_product();
CREATE OR REPLACE FUNCTION get_product()
    RETURNS TABLE (
        id INTEGER,
        name text,
        proteins NUMERIC,
        fats NUMERIC,
        carbohydrates NUMERIC,
        kilocalories NUMERIC
    ) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT * FROM product;
    END;
    $$
LANGUAGE plpgsql;


--Получение данных по всем приемам пищи --
DROP FUNCTION IF EXISTS get_meal_macro(INTEGER, DATE);
CREATE OR REPLACE FUNCTION get_meal_macro(curr_user_id INTEGER, curr_date DATE)
    RETURNS TABLE (
        proteins NUMERIC,
        fats NUMERIC,
        carbohydrates NUMERIC,
        kilocalories NUMERIC
    ) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT meal.proteins, meal.fats, meal.carbohydrates, meal.kilocalories FROM meal
        WHERE user_id = curr_user_id AND date = curr_date
        ORDER BY meal_type;
    END;
    $$
LANGUAGE plpgsql;


-- Получение цели человека --
DROP FUNCTION IF EXISTS get_user_goal(INT);
CREATE OR REPLACE FUNCTION get_user_goal(curr_user_id INT)
    RETURNS TEXT AS
    $$
    DECLARE
        user_goal TEXT;
    BEGIN
        SELECT goal INTO user_goal
        FROM user_info
        WHERE id = curr_user_id;

        RETURN user_goal;
    END;
    $$
LANGUAGE plpgsql;


-- Получение данных об пользователе --
DROP FUNCTION IF EXISTS get_user_info(INTEGER);
CREATE OR REPLACE FUNCTION get_user_info(curr_user_id INTEGER)
    RETURNS TABLE (
        gender VARCHAR(6),
        activity VARCHAR(10),
        weight numeric,
        height numeric,
        age INTEGER
    ) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT us_in.gender, us_in.activity, us_in.weight, us_in.height, us_in.age
        FROM user_info us_in
        WHERE id = curr_user_id;
    END;
    $$
LANGUAGE plpgsql;


-- Получение статистики пользователя --
DROP FUNCTION IF EXISTS get_user_statistic(INTEGER, DATE);
CREATE OR REPLACE FUNCTION get_user_statistic(curr_user_id INTEGER, curr_date DATE)
    RETURNS TABLE (
        id INTEGER,
        user_id INTEGER,
        proteins_intake numeric,
        fats_intake numeric,
        carbohydrates_intake numeric,
        kilocalories_intake numeric,
        weight_loss numeric,
        date DATE
    ) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT * FROM user_statistic
        WHERE user_statistic.user_id = curr_user_id AND user_statistic.date = curr_date;
    END;
    $$
LANGUAGE plpgsql;


-- Получение конечной информации об пользователе --
DROP FUNCTION IF EXISTS find_user_data(INTEGER);
CREATE OR REPLACE FUNCTION find_user_data(curr_account_id INTEGER)
    RETURNS TABLE (
        username VARCHAR(15),
        gender VARCHAR(6),
        activity VARCHAR(10),
        weight NUMERIC,
        height NUMERIC,
        age INTEGER,
        goal TEXT
    ) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT
            acc.username,
            us.gender, us.activity, us.weight, us.height, us.age, us.goal
        FROM account acc
        JOIN user_info us ON acc.id = us.account_id
        WHERE us.account_id = curr_account_id;
    END;
    $$
LANGUAGE plpgsql;



