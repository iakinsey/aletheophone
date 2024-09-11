from aiosqlite import connect, Connection
from fastapi import Depends, FastAPI
from sqlite_vec import loadable_path
from .config import get_config, Config
from .gateway.data import DataGateway
from .model.note import Note

MODELS = [Note]


def config() -> Config:
    return get_config()


async def db_conn(config: Config = Depends(config)) -> Connection:
    conn = await connect(config.db_path)

    await conn.enable_load_extension(True)
    await conn.load_extension(loadable_path())
    await conn.enable_load_extension(False)
    await conn.execute("PRAGMA journal_mode=WAL;")

    return conn


async def db(db_conn=Depends(db_conn)) -> DataGateway:
    gateway = DataGateway(db_conn)

    for model in MODELS:
        await gateway.declare(model)

    return gateway
