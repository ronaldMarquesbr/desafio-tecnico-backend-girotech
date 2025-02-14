from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from src.main.factories.exchange_rate import exchange_rate_factory
from src.main.schemas.exchange_rate import ExchangeRateBase


exchange_rate_bp = Blueprint('exchange_rate', __name__)


@exchange_rate_bp.route('/exchange-rates', methods=['POST'])
def create_exchange_rate():
    try:
        exchange_rate_data = ExchangeRateBase(**request.json)

        exchange_rate = exchange_rate_factory(exchange_rate_data)

        return jsonify(exchange_rate.to_dict()), 200

    except ValidationError as e:
        return jsonify({
            'error': e.errors()
        }), 400
