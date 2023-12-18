------ Обновление данных таблиц ------

-- Обновление пароля таблицы account --
DROP FUNCTION IF EXISTS change_password(varchar(20), varchar(15));
CREATE OR REPLACE FUNCTION change_password(p_password varchar(20), p_username varchar(15))
    RETURNS VOID AS
    $$
    BEGIN
        UPDATE account SET password = p_password WHERE username = p_username;
    END;
    $$
LANGUAGE plpgsql;

-- Обновление информации об приеме пищи --
DROP FUNCTION IF EXISTS update_meal_info(VARCHAR(10), DATE, NUMERIC, NUMERIC, NUMERIC, NUMERIC, INT);
CREATE OR REPLACE FUNCTION update_meal_info(
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
        UPDATE meal SET proteins = curr_proteins, fats = curr_fats,
                        carbohydrates = curr_carbohydrates, kilocalories = curr_kilocalories
        WHERE meal_type = curr_meal_type AND date = curr_date AND user_id = curr_user_id;
    END;
    $$
LANGUAGE plpgsql;


-- Обновление статистики пользователя за день --
DROP FUNCTION IF EXISTS update_statistic_info(numeric, numeric, numeric, numeric, DATE, numeric, INTEGER);
CREATE OR REPLACE FUNCTION update_statistic_info(
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
        UPDATE user_statistic SET proteins_intake = curr_proteins, fats_intake = curr_fats,
                        carbohydrates_intake = curr_carbohydrates, kilocalories_intake = curr_kilocalories,
                        weight_loss = curr_weight_loss
        WHERE date = curr_date AND user_id = curr_user_id;
    END;
    $$
LANGUAGE plpgsql;

-- Обновление имени пользователя --
DROP FUNCTION IF EXISTS update_username(varchar(15), INTEGER);
CREATE OR REPLACE FUNCTION update_username(
    new_username varchar(15),
    curr_account_id INTEGER
)
    RETURNS VOID AS
    $$
    BEGIN
        UPDATE account SET username = new_username WHERE id = curr_account_id;
    END;
    $$
LANGUAGE plpgsql;

-- Обновление основной информации об пользователе --
DROP FUNCTION IF EXISTS update_user_info(INTEGER, varchar(8), numeric, numeric, TEXT, INTEGER);
CREATE OR REPLACE FUNCTION update_user_info(
    new_age INTEGER,
    curr_gender varchar(8),
    new_weight numeric,
    new_height numeric,
    new_goal TEXT,
    user_id INTEGER
)
    RETURNS VOID AS
    $$
    BEGIN
        UPDATE user_info SET age = new_age, gender = curr_gender,
                             weight = new_weight, height = new_height, goal = new_goal
        WHERE account_id = user_id;
    END;
    $$
LANGUAGE plpgsql;