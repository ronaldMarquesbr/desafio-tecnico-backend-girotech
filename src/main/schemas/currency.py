from pydantic import BaseModel, constr


class CurrencySchema(BaseModel):
    name: constr(min_length=3, max_length=50)
    type: constr(min_length=1, max_length=80)
