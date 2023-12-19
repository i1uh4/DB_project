from app.database.config import DBConfig
import yaml


def get_database_config() -> DBConfig:
    with open("config.yaml") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    database: dict = cfg["database"]
    return DBConfig(
        user=database["user"],
        password=database["password"],
        database=database.get("dbname") or "postgres",
        host=database.get("host") or "localhost",
        port=database.get("port") or "5432",
    )
