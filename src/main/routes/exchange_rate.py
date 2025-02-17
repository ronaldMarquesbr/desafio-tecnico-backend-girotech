from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from src.main.factories.exchange_rate_factory import exchange_rate_factory
from src.main.schemas.exchange_rate import ExchangeRateBase, ExchangeRateUpdateBase
from src.models.exchange_rate import ExchangeRate
from src.models.currency import Currency


exchange_rate_bp = Blueprint('exchange_rate', __name__)


@exchange_rate_bp.route('/exchange-rates', methods=['POST'])
def create_exchange_rate():
    try:
        exchange_rate_data = ExchangeRateBase(**request.json)

        is_valid_currency_id = Currency.query.filter_by(id=exchange_rate_data.currency_id).scalar() is not None

        if not is_valid_currency_id:
            return jsonify({'error': 'Currency id does not exist'}), 404

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


@exchange_rate_bp.route('/exchange-rates/old', methods=['DELETE'])
def delete_old_exchange_rates():
    deleted_exchange_rates_count = ExchangeRate.delete_old_exchange_rates()

    if deleted_exchange_rates_count == 0:
        return jsonify({'message': 'No exchange rates older than 30 days found'}), 200

    return jsonify({'message': f'{deleted_exchange_rates_count} exchange rates older than 30 days were deleted'}), 200
