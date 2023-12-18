from dataclasses import dataclass


@dataclass
class DBConfig:
    user: str
    password: str
    database: str
    host: str
    port: str

    def to_dict(self):
        return {
            "user": self.user,
            "password": self.password,
            "dbname": self.database,
            "host": self.host,
            "port": self.port,
        }

    def to_connection_string(self):
        return f"dbname={self.database} user={self.user} password={self.password}"
