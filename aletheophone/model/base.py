from pydantic import BaseModel


class DataModel(BaseModel):
    def schema(self):
        raise NotImplementedError

    @classmethod
    def keys(cls):
        return tuple(cls.__fields__.keys())

    def values(self):
        data_dict = self.model_dump()
        return tuple(data_dict.values())

    @classmethod
    def sql_keys(cls, filter: set = set()):
        keys = [k for k in cls.keys() if k not in filter]

        return ", ".join(keys)

    def sql_values(self, filter: set = set()):
        keys = [k for k in self.keys() if k not in filter]

        return ",".join(["?" for _ in keys])

    @classmethod
    def from_row(cls, row: list):
        return cls(**dict(zip(cls.keys(), row)))
