from pydantic import BaseModel, model_validator
from pydantic_core import PydanticCustomError
from typing import Optional
from datetime import date as datetype


class ExchangeRateBase(BaseModel):
    date: datetype
    daily_variation: float
    daily_rate: float
    currency_id: int


class ExchangeRateUpdateBase(BaseModel):
    date: Optional[datetype] = None
    daily_variation: Optional[float] = None
    daily_rate: Optional[float] = None
    currency_id: Optional[int] = None

    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_field(cls, data):
        if not any(data.values()):
            raise PydanticCustomError('Missing data', 'at least one field must be provided')

        return data
