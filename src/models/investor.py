from src.drivers.database import db
from src.models.investment_history import InvestmentHistory


class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    @classmethod
    def remove_investor(cls, investor_id):
        investor = cls.query.get(investor_id)

        if not investor:
            return "Investor not found"

        db.session.query(InvestmentHistory).filter(
            InvestmentHistory.investor_id == investor_id
        ).delete(synchronize_session="fetch")

        db.session.delete(investor)
        db.session.commit()

        return None
