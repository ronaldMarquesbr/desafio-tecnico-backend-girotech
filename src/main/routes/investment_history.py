from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from src.main.schemas.investment_history import InvestmentHistoryBase
from src.main.factories.investment_history_factory import investment_history_factory

investment_history_bp = Blueprint('investment_history', __name__)


@investment_history_bp.route('/investments', methods=['POST'])
def create_investment_history():
    try:
        investment_data = InvestmentHistoryBase(**request.json)

    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    investment_history = investment_history_factory(investment_data)

    return jsonify(investment_history.to_dict()), 200
