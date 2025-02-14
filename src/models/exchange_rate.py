from sqlalchemy import func
from src.drivers.database import db


class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, server_default=func.now(), nullable=False)
    daily_variation = db.Column(db.Float, nullable=False)
    daily_rate = db.Column(db.Float, nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)

    currency = db.relationship('Currency')

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'daily_variation': self.daily_variation,
            'daily_rate': self.daily_rate,
            'currency_id': self.currency_id,
        }
