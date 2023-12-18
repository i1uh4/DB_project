from app.database.database import DataBase
from app.gui.gui import AuthorizationWindow
from app.settings.config import get_database_config


def main():
    config = get_database_config()
    database = DataBase(config)
    window = AuthorizationWindow(database)
    window.run()


if __name__ == "__main__":
    main()
