from src.drivers.database import db
from src.models.investment_history import InvestmentHistory
from src.main.schemas.investment_history import InvestmentHistoryBase


def investment_history_factory(investment_history: InvestmentHistoryBase) -> InvestmentHistory:
    new_investment_history = InvestmentHistory(
        initial_amount=investment_history.initial_amount,
        months=investment_history.months,
        interest_rate=investment_history.interest_rate,
        final_amount=investment_history.final_amount,
        currency_id=investment_history.currency_id,
        investor_id=investment_history.investor_id
    )

    db.session.add(new_investment_history)
    db.session.commit()

    return new_investment_history
