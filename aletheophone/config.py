from pydantic import BaseModel
from os import getcwd, makedirs
from os.path import exists, join

data_path = join(getcwd(), "data")
_CONFIG = None


class Config(BaseModel):
    storage_path: str = data_path
    db_path: str = join(data_path, "mg.db")
    http_host: str = "0.0.0.0"
    http_port: int = 8000


def set_config(config: Config):
    global _CONFIG

    _CONFIG = config

    makedirs(config.storage_path, exist_ok=True)


def get_config() -> Config:
    global _CONFIG

    if _CONFIG:
        return _CONFIG

    path = join(getcwd(), "config.json")
    config = Config()

    if exists(path):
        config_json = open(path, "r").read().strip()
        config = Config.model_validate_json(config_json)

    makedirs(config.storage_path, exist_ok=True)

    _CONFIG = config

    return config
