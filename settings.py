from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Sber:
    sber_auth: str


@dataclass
class Database:
    async_db_url: str
    db_url: str
    db_echo: bool


@dataclass
class Settings:
    bots: Bots
    db: Database
    sber: Sber


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('BOT_TOKEN'),
            admin_id=env.int('ADMIN_ID')
        ),
        db=Database(
            async_db_url=env.str('DATABASE_URL_ASYNC'),
            db_url=env.str('DATABASE_URL'),
            db_echo=env.bool('DB_ECHO')
        ),
        sber=Sber(
            sber_auth=env.str('SBER_AUTH'),
        ),
    )


settings = get_settings('.env')