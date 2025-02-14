import pydantic.networks
from pydantic import EmailStr, BaseModel, constr

pydantic.networks.MAX_EMAIL_LENGTH = 80


class InvestorSchema(BaseModel):
    name:  constr(min_length=3, max_length=80)
    email: EmailStr
