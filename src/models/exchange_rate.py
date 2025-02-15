from sqlalchemy import func
from datetime import date, timedelta
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
