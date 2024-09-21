from datetime import timedelta
from time import time
from typing import Any
from numpy import float32
from .base import DataModel
from ..util.data import deserialize_float32
from ..util.encoder import Encoder


encoder = Encoder()


class Note(DataModel):
    id: int
    text: str
    vector: Any
    created: int

    def model_dump(self, **kwargs):
        kwargs["exclude"] = {"vector"}
        return super().model_dump(**kwargs)

    @classmethod
    def schema(cls):
        return """
            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                vector FLOAT[1024] NOT NULL,
                created INTEGER NOT NULL DEFAULT (CAST(strftime('%s', 'now') AS INTEGER))
            );
        """

    @classmethod
    async def create(cls, text: str):
        keys = cls.sql_keys({"id", "created"})
        values = cls.sql_values({"id", "created"})
        encoded = await encoder.encode([text])
        row = (text, encoded[0].astype(float32))

        return (
            f"INSERT INTO note ({keys}) VALUES ({values}) RETURNING {cls.sql_keys()}",
            row,
        )

    def delete(self):
        return (f"DELETE FROM note WHERE id = ?", (self.id,))

    @classmethod
    def get(cls, id: int):
        return (f"SELECT {cls.sql_keys()} FROM note WHERE id = ? LIMIT 1", (id,))

    @classmethod
    def list(
        cls, order_by: str, order: str, limit: int, offset: int, window: timedelta
    ):

        time_window = int(time() - window.total_seconds())
        return f"""
            SELECT {cls.sql_keys()} FROM note
            WHERE
                created >= {time_window}
            ORDER BY {order_by} {order}
            LIMIT {limit}
            OFFSET {offset}
        """

    @classmethod
    def from_row(cls, row: list):
        if not row:
            return None

        params = dict(zip(cls.keys(), row))
        params["vector"] = deserialize_float32(params["vector"])

        return cls(**params)
