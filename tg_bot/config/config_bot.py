from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass
class DataPath:
    path: str


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    data_path: DataPath


def load_config() -> Config:
    """
    Для работы с конфигом (теми данные, которые не должны публиковаться).
    Например API Бота или информация о пути к json файлу с данными
    :return:
    """
    load_dotenv()
    return Config(tg_bot=TgBot(token=getenv("BOT_API_KEY")),
                  data_path=DataPath(path=getenv("DATA")))
