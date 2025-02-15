from sqlalchemy import func
from datetime import date, timedelta
from src.models.currency import Currency
from src.drivers.database import db


class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, server_default=func.now(), nullable=False)
    daily_variation = db.Column(db.Float, nullable=False)
    daily_rate = db.Column(db.Float, nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)

    currency = db.relationship('Currency')

    def to_dict(self):
        formatted_date = self.date.strftime('%Y-%m-%d')

        return {
            'id': self.id,
            'date': formatted_date,
            'daily_variation': self.daily_variation,
            'daily_rate': self.daily_rate,
            'currency_name': self.currency.name,
            'currency_type': self.currency.type
        }

    @classmethod
    def get_recent_exchange_rates(cls):
        period_start = date.today() - timedelta(days=6)
        exchange_rates = cls.query.filter(cls.date >= period_start).order_by(cls.date.desc()).all()
        recent_exchange_rates = [exchange_rate.to_dict() for exchange_rate in exchange_rates]

        return recent_exchange_rates

    @classmethod
    def update_exchange_rate(cls, exchange_rate_id, data):
        exchange_rate = cls.query.get(exchange_rate_id)

        if not exchange_rate:
            return None, "Exchange rate not found"

        if data.date:
            exchange_rate.date = data.date

        if data.daily_variation:
            exchange_rate.daily_variation = data.daily_variation

        if data.daily_rate:
            exchange_rate.daily_rate = data.daily_rate

        if data.currency_id:
            new_currency = Currency.query.get(data.currency_id)

            if not new_currency:
                return None, "Currency not found"

            exchange_rate.currency_id = new_currency.id

        db.session.commit()

        return exchange_rate, None

    @classmethod
    def delete_old_exchange_rates(cls):
        period_start_date = date.today() - timedelta(days=29)

        deleted_count = db.session.query(ExchangeRate).filter(
            ExchangeRate.date <= period_start_date
        ).delete(synchronize_session="fetch")

        db.session.commit()

        return deleted_count
