from pydantic import BaseModel
from datetime import date


class ExchangeRateBase(BaseModel):
    date: date
    daily_variation: float
    daily_rate: float
    currency_id: int
