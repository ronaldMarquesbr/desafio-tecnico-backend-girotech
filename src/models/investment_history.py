from src.drivers.database import db


class InvestmentHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initial_amount = db.Column(db.Float, nullable=False)
    months = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    final_amount = db.Column(db.Float, nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    investor_id = db.Column(db.Integer, db.ForeignKey('investor.id'), nullable=False)

    currency = db.relationship('Currency')
    investor = db.relationship('Investor')

    def to_dict(self):
        return {
            'id': self.id,
            'initial_amount': self.initial_amount,
            'months': self.months,
            'interest_rate': self.interest_rate,
            'final_amount': self.final_amount,
            'currency_id': self.currency_id,
            'investor_id': self.investor_id,
        }
