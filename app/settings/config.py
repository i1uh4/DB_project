import os
from dotenv import load_dotenv
from app.database.config import DBConfig

load_dotenv()


def get_database_config() -> DBConfig:
    return DBConfig(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.getenv("DB_NAME", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )
