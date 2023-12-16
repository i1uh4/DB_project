CREATE OR REPLACE FUNCTION update_user_statistic()
RETURNS TRIGGER AS $$
DECLARE
    curr_user INT;
    curr_date DATE;
    total_proteins numeric;
    total_fats numeric;
    total_carbohydrates numeric;
    total_kilocalories numeric;

    activity_coef CONSTANT jsonb = '{"Very low": 1.2, "Low": 1.375, "Medium": 1.55, "High": 1.725, "Very high": 1.9}';
    user_sex VARCHAR(6);
    user_activity VARCHAR(10);
    user_weight numeric;
    user_height numeric;
    user_age INTEGER;
    user_BMR numeric;
    user_AMR numeric;
    user_weight_loss numeric;
BEGIN
    SELECT user_id, date
    INTO curr_user, curr_date
    FROM meal
    WHERE id = NEW.id;

    -- Вычисляем сумму значений для каждого meal_type в указанную дату и для указанного пользователя
    SELECT
        COALESCE(SUM(proteins), 0),
        COALESCE(SUM(fats), 0),
        COALESCE(SUM(carbohydrates), 0),
        COALESCE(SUM(kilocalories), 0)
    INTO
        total_proteins,
        total_fats,
        total_carbohydrates,
        total_kilocalories
    FROM
        meal
    WHERE
        user_id = curr_user AND date = curr_date;

    -- Получаем информацию о пользователе
    SELECT gender, activity, weight, height, age
    INTO user_sex, user_activity, user_weight, user_height, user_age
    FROM get_user_info(curr_user);

    -- Рассчитываем BMR и AMR
    user_BMR := CASE WHEN user_sex = 'female' THEN 655.1 + (9.563 * user_weight) + (1.850 * user_height) - (4.676 * user_age)
                ELSE 66.47 + (13.75 * user_weight) + (5.003 * user_height) - (6.755 * user_age)
           END;

    user_AMR := user_BMR * (activity_coef->user_activity)::numeric;

    -- Рассчитываем user_weight_loss
    user_weight_loss := total_kilocalories - user_AMR;

    -- Обновляем статистику пользователя при вставке новой записи в таблицу meal
    UPDATE user_statistic
    SET
        proteins_intake = total_proteins,
        fats_intake = total_fats,
        carbohydrates_intake = total_carbohydrates,
        kilocalories_intake = total_kilocalories,
        weight_loss = user_weight_loss / 7700
    WHERE
        user_id = curr_user AND date = curr_date;

    -- Если запись для указанного пользователя и даты не существует, создаем новую
    IF NOT FOUND THEN
        INSERT INTO user_statistic (user_id, proteins_intake, fats_intake, carbohydrates_intake, kilocalories_intake, date)
        VALUES (curr_user, total_proteins, total_fats, total_carbohydrates, total_kilocalories, curr_date);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Обновленный триггер
CREATE OR REPLACE TRIGGER meal_insert_update_trigger
AFTER INSERT OR UPDATE ON meal
FOR EACH ROW
EXECUTE FUNCTION update_user_statistic();
