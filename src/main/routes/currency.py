from flask import Blueprint, jsonify, request
from sqlalchemy import or_, exists
from src.drivers.database import db
from src.main.schemas.currency import CurrencySchema
from src.models.currency import Currency
from src.main.factories.currency_factory import currency_factory
from pydantic import ValidationError


currency_bp = Blueprint('currency', __name__)


@currency_bp.route('/currencies', methods=['POST'])
def create_currency():
    try:
        currency_data = CurrencySchema(**request.json)

        existing_currency = db.session.query(
            exists().where(
                or_(Currency.name == currency_data.name, Currency.type == currency_data.type)
            )
        ).scalar()

        if existing_currency:
            return jsonify({'message': 'Currency name or type already exists'}), 400

        currency = currency_factory(currency_data)

        return jsonify(currency.to_dict()), 200

    except ValidationError as e:
        return jsonify({
            "error": e.errors()
        }), 400


@currency_bp.route('/currencies', methods=['GET'])
def get_currencies():
    currencies = Currency.query.all()
    currency_list = [currency.to_dict() for currency in currencies]

    return jsonify(currency_list), 200
