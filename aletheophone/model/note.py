from datetime import timedelta
from time import time
from numpy import float32
from sqlite_vec import serialize_float32
from .base import DataModel
from ..util.encoder import Encoder


encoder = Encoder()


class Note(DataModel):
    id: int
    text: str
    vector: list[float]
    created: int

    def model_dump_json(self, **kwargs):
        kwargs.setdefault("exclude", {"vector"})
        return super().model_dump_json(**kwargs)

    def json(self, **kwargs):
        kwargs.setdefault("exclude", {"vector"})
        return super().json(**kwargs)

    def schema(self):
        return """
            CREATE TABLE IF NOT EXISTS note (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                vector FLOAT[1024] NOT NULL,
                created INT NOT NULL DEFAULT (CAST(strftime('%s', 'now') AS INTEGER))
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
            LIMIT {limit}
            OFFSET {offset}
            ORDER BY {order_by} {order}
        """
