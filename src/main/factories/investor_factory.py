from src.drivers.database import db
from src.models.investor import Investor
from src.main.schemas.investor import InvestorSchema


def investor_factory(investor: InvestorSchema) -> Investor:
    new_investor = Investor(name=investor.name, email=investor.email)
    db.session.add(new_investor)
    db.session.commit()

    return new_investor
