from pydantic import BaseModel
from os import getcwd, makedirs
from os.path import exists, join

data_path = join(getcwd(), "data")


class Config(BaseModel):
    storage_path: str = data_path
    db_path: str = join(data_path, "mg.db")
    http_host: str = "0.0.0.0"
    http_port: int = 8000


def get_config() -> Config:
    path = join(getcwd(), "config.json")
    config = Config()

    if exists(path):
        config_json = open(path, "r").read().strip()
        config = Config.model_validate_json(config_json)

    makedirs(config.storage_path, exist_ok=True)

    return config
