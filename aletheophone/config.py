from pydantic import BaseModel
from os import getcwd, makedirs
from os.path import join

data_path = join(getcwd(), "data")


class Config(BaseModel):
    storage_path: str = data_path
    db_path: str = join(data_path, "mg.db")


def get_config() -> Config:
    config_json = open(join(getcwd(), "config.json"), "r").read().strip()
    config = Config.model_validate_json(config_json)

    makedirs(config.storage_path, exist_ok=True)

    return config
