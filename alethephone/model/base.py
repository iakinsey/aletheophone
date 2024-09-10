from pydantic import BaseModel


class DataModel(BaseModel):
    @property
    def schema(self):
        raise NotImplementedError

    @classmethod
    def keys(cls):
        return tuple(cls.__fields__.keys())

    def values(self):
        data_dict = self.model_dump()
        return tuple(data_dict.values())

    @classmethod
    def sql_keys(slf):
        return ", ".join(cls.keys())

    def sql_values(self):
        return ",".join(["?" for _ in self.keys])
