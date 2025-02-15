from src.drivers.database import db
from src.models.exchange_rate import ExchangeRate
from src.main.schemas.exchange_rate import ExchangeRateBase


def exchange_rate_factory(exchange_rate: ExchangeRateBase) -> ExchangeRate:
    new_exchange_rate = ExchangeRate(
                            daily_variation=exchange_rate.daily_variation,
                            daily_rate=exchange_rate.daily_rate,
                            date=exchange_rate.date,
                            currency_id=exchange_rate.currency_id,
                        )

    db.session.add(new_exchange_rate)
    db.session.commit()

    return new_exchange_rate
