------ Очистка таблиц ------

-- Удаление всех таблиц
DROP FUNCTION IF EXISTS clear_all_tables();
CREATE FUNCTION clear_all_tables()
	RETURNS void AS
	$$
        DELETE FROM product;
        DELETE FROM user_info;
        DELETE FROM user_statistic;
        DELETE FROM favourites;
        DELETE FROM account;
        DELETE FROM meal;
	$$
LANGUAGE sql;

-- Удаление таблицы account

DROP FUNCTION IF EXISTS clear_account_table(INTEGER);
CREATE FUNCTION clear_account_table(curr_account_id INTEGER)
	RETURNS void AS
	$$
	DELETE FROM account
    WHERE id = curr_account_id;
	$$
LANGUAGE sql;

-- Удаление продукта из категории избранное --
DROP FUNCTION IF EXISTS delete_fav_product(INTEGER, INTEGER);
CREATE FUNCTION delete_fav_product(curr_user_id INTEGER, curr_product_id INTEGER)
	RETURNS void AS
	$$
	DELETE FROM favourites
    WHERE user_id = curr_user_id AND product_id = curr_product_id;
	$$
LANGUAGE sql;




