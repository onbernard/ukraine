from io import (
    BytesIO,
)
from typing import (
    Dict,
)

from redis_om import (
    JsonModel,
)
from pydantic import (
    root_validator,
)
import polars as pl

from commons.models.base import BaseModel


class AvroDF(BaseModel):
    data:bytes

    class Config:
        arbitrary_types_allowed=True
        extra="ignore"
        json_encoders = {
            bytes: lambda v: v.hex()
        }
    
    def __repr__(self) -> str:
        return self.df.__repr__()
    
    @root_validator(pre=True)
    def root(cls, values:Dict):
        if "data" not in values:
            assert "df" in values, "a dataframe should be provided"
            df:pl.DataFrame = values.get("df")
            values["data"] = cls.serialize_df(df)
        elif isinstance(values["data"],str): # Data coming from json
            data:str = values.get("data")
            values["data"] = bytes.fromhex(data)
        return values
    
    @staticmethod
    def serialize_df(v:pl.DataFrame)->bytes:
        with BytesIO() as btio:
            v.write_avro(btio)
            return btio.getbuffer().tobytes()
    
    @staticmethod
    def deserialize_df(bt:bytes)->pl.DataFrame:
        with BytesIO() as btio:
            btio.write(bt)
            btio.seek(0)
            return pl.read_avro(btio)
    
    @property
    def df(self)->pl.DataFrame:
        return self.deserialize_df(self.data)