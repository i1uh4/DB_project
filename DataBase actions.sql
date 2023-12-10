DROP EXTENSION IF EXISTS dblink;
CREATE EXTENSION IF NOT EXISTS dblink;

DROP FUNCTION IF EXISTS create_db(text, text);
CREATE OR REPLACE FUNCTION create_db(dbname text)
RETURNS VOID AS
    $$
    BEGIN
        IF EXISTS (SELECT datname FROM pg_database WHERE datname = dbname) THEN
             RAISE NOTICE 'Database already exists';
        ELSE
             PERFORM dblink_exec('user=postgres password=123 dbname= ' || current_database(),
                    'CREATE DATABASE ' || dbname);

          PERFORM dblink_exec('user=postgres password=123 dbname= ' || dbname,
          '
                        CREATE TABLE IF NOT EXISTS account (
                            id SERIAL PRIMARY KEY,
                            username varchar(15) NOT NULL UNIQUE,
                            password varchar(20) NOT NULL
                        );

                        CREATE TABLE IF NOT EXISTS user_info (
                            id SERIAL PRIMARY KEY,
                            gender varchar(6) NOT NULL,
                            activity varchar(10) NOT NULL,
                            age integer NOT NULL CHECK(age > 0),
                            weight numeric NOT NULL CHECK(weight > 0),
                            height numeric NOT NULL CHECK(height > 0),
                            goal text,
                            account_id integer NOT NULL UNIQUE,
                            FOREIGN KEY (account_id) REFERENCES account (id) ON DELETE CASCADE
                        );

                        CREATE TABLE IF NOT EXISTS user_statistic (
                            id SERIAL PRIMARY KEY,
                            user_id integer NOT NULL,
                            proteins_intake numeric NOT NULL DEFAULT 0,
                            fats_intake numeric NOT NULL DEFAULT 0,
                            carbohydrates_intake numeric NOT NULL DEFAULT 0,
                            kilocalories_intake numeric NOT NULL DEFAULT 0,
                            weight_loss numeric NOT NULL DEFAULT 0,
                            date DATE NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES user_info (id) ON DELETE CASCADE
                        );

                        CREATE TABLE IF NOT EXISTS product (
                            id SERIAL PRIMARY KEY,
                            name TEXT NOT NULL,
                            proteins numeric NOT NULL,
                            fats numeric NOT NULL,
                            carbohydrates numeric NOT NULL,
                            kilocalories numeric NOT NULL
                        );

                        CREATE TABLE IF NOT EXISTS favourites (
                            id SERIAL PRIMARY KEY,
                            user_id integer NOT NULL,
                            product_id integer NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES user_info (id) ON DELETE CASCADE,
                            FOREIGN KEY (product_id) REFERENCES product (id)
                        );

                        CREATE TABLE IF NOT EXISTS meal (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            meal_type VARCHAR(10) NOT NULL,
                            date DATE NOT NULL,
                            proteins numeric,
                            fats numeric,
                            carbohydrates numeric,
                            kilocalories numeric NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE
                        );
          ');
        END IF;
    END;
    $$
LANGUAGE plpgsql;

---- Подключение к базе данных ----
DROP FUNCTION IF EXISTS connect_to_database(text);
CREATE OR REPLACE FUNCTION connect_to_database(dbname text)
RETURNS VOID AS
$$
BEGIN
    PERFORM dblink_connect('user=postgres password=123 dbname=' || dbname);
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Failed to connect to the database %', dbname;
END;
$$
LANGUAGE plpgsql;


---- Удаление всей базы данных ----
DROP FUNCTION IF EXISTS drop_db(text);
CREATE FUNCTION drop_db(dbname text)
	RETURNS INTEGER AS
	$func$
	BEGIN
		IF EXISTS (SELECT datname FROM pg_database WHERE datname = dbname) THEN
   			PERFORM dblink_exec('user=postgres password=123 dbname=' || dbname,
								'DROP DATABASE ' || quote_ident(dbname));
			RETURN 1;
		ELSE
			RAISE NOTICE 'Database does not exist';
			RETURN 0;
		END IF;

	END
	$func$
	LANGUAGE plpgsql;
