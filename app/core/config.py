from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class DB(BaseSettings):
    user: str
    password:str
    host: str
    port: int

    @property
    def database_url(self) -> str:
        return ...


class PG(DB):
    db: str
    pool_size: int = 5 # Максимальное количество единовременных подключений

    @property
    def database_url(self) -> str:
        # DSN
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"



class Config(BaseSettings):
    model_config = SettingsConfigDict( env_nested_delimiter='__')

    environment: Literal["DEV"] | Literal["TEST"] = "DEV"
    project_name: str
    project_host: str
    project_port: int

    pg: PG

    @property
    def debug(self) -> bool:
        return self.environment == "TEST"

if __name__ == '__main__':
    cfg:Config = Config()
    print(cfg.pg.database_url_asyncpg)
