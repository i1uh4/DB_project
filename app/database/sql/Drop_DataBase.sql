---- Удаление всей базы данных ----
CREATE EXTENSION IF NOT EXISTS dblink;

DROP FUNCTION IF EXISTS drop_db(VARCHAR(255), VARCHAR(255), text, VARCHAR(255));
CREATE OR REPLACE FUNCTION drop_db(username VARCHAR(255), password VARCHAR(255), dbname text, db_user VARCHAR(255))
RETURNS VOID AS
$$
BEGIN
	PERFORM dblink_exec(format('user=postgres password=123'),
							'DROP DATABASE IF EXISTS ' || quote_ident(dbname));
   	PERFORM dblink_exec(format('user=postgres password=123'),
							format('DROP USER IF EXISTS %I', db_user));
END;
$$
LANGUAGE plpgsql;