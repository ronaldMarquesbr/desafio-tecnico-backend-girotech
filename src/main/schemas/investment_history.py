from pydantic import BaseModel


class InvestmentHistoryBase(BaseModel):
    initial_amount: int
    months: int
    interest_rate: float
    final_amount: float
    currency_id: int
    investor_id: int
