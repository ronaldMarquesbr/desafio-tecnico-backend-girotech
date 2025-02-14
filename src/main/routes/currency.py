from flask import Blueprint, jsonify, request
from sqlalchemy import or_, exists
from src.models.currency import Currency
from src.drivers.database import db

currency_bp = Blueprint('currency', __name__)


@currency_bp.route('/currencies', methods=['POST'])
def create_currency():
    data = request.json
    currency_name = data.get('name')
    currency_type = data.get('type')

    if currency_name and currency_type:
        # Checar se nome ou tipo já estão sendo utilizados
        existing_currency = db.session.query(
            exists().where(
                or_(Currency.name == currency_name, Currency.type == currency_type)
            )
        ).scalar()

        if existing_currency:
            return jsonify({'message': 'Currency name or type already exists'}), 400

        currency = Currency(name=currency_name, type=currency_type)
        db.session.add(currency)
        db.session.commit()

        return jsonify({
            'id': currency.id,
            'name': currency.name,
            'type': currency.type
        })

    else:
        errors = {}
        
        if 'name' not in data:
            errors['name'] = 'this field is required'

        if 'type' not in data:
            errors['type'] = 'this field is required'

        return jsonify({
            'message': 'Invalid data request', 'errors': errors
        }), 400
