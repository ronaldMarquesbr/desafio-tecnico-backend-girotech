from src.drivers.database import db
from src.models.currency import Currency
from src.main.schemas.currency import CurrencySchema


def currency_factory(currency: CurrencySchema) -> Currency:
    currency_name = currency.name
    currency_type = currency.type
    new_currency = Currency(name=currency_name, type=currency_type)

    db.session.add(new_currency)
    db.session.commit()

    return new_currency
