from .base import DataModel


class Note(DataModel):
    id: int
    text: str
    vector: list[float]

    @property
    def schema(self):
        return """
            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                vector FLOAT[1024] NOT NULL
            );
        """

    @property
    def create(self):
        return (
            f"INSERT INTO note ({self.sql_keys}) VALUES ({self.sql_values})",
            self.values,
        )

    @property
    def delete(self):
        return (f"DELETE FROM note WHERE id = ?", (self.id,))

    @staticmethod
    @property
    def get(id: int):
        return (f"SELECT {self.sql_keys} FROM note WHERE id = ?", (id,))
