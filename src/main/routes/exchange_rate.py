from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from src.main.factories.exchange_rate import exchange_rate_factory
from src.main.schemas.exchange_rate import ExchangeRateBase, ExchangeRateUpdateBase
from src.models.exchange_rate import ExchangeRate


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


@exchange_rate_bp.route('/exchange-rates/recent', methods=['GET'])
def get_recent_exchange_rates():
    recent_exchange_rates = ExchangeRate.get_recent_exchange_rates()

    return jsonify(recent_exchange_rates)


@exchange_rate_bp.route('/exchange-rates/<int:exchange_rate_id>', methods=['PATCH'])
def update_exchange_rate(exchange_rate_id):
    try:
        data = ExchangeRateUpdateBase(**request.json)
        exchange_rate, error = ExchangeRate.update_exchange_rate(exchange_rate_id, data)

        if error:
            return jsonify({'error': error}), 404

        return jsonify(exchange_rate.to_dict()), 200

    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

