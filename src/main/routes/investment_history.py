from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from src.main.schemas.investment_history import InvestmentHistoryBase
from src.main.factories.investment_history_factory import investment_history_factory
from src.models.currency import Currency
from src.models.investor import Investor

investment_history_bp = Blueprint('investment_history', __name__)


@investment_history_bp.route('/investments', methods=['POST'])
def create_investment_history():
    try:
        investment_data = InvestmentHistoryBase(**request.json)

    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    is_valid_currency_id = Currency.query.filter_by(id=investment_data.currency_id).scalar() is not None

    if not is_valid_currency_id:
        return jsonify({'error': 'Currency id does not exist'}), 404

    is_valid_investor_id = Investor.query.filter_by(id=investment_data.investor_id).scalar() is not None

    if not is_valid_investor_id:
        return jsonify({'error': 'Investor id does not exist'}), 404

    investment_history = investment_history_factory(investment_data)

    return jsonify(investment_history.to_dict()), 200
