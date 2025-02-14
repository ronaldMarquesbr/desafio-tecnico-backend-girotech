from flask import Blueprint, jsonify, request
from sqlalchemy import exists
from src.main.schemas.investor import InvestorSchema
from src.main.factories.investor_factory import investor_factory
from src.drivers.database import db
from src.models.investor import Investor
from pydantic import ValidationError

investor_bp = Blueprint('investor', __name__)


@investor_bp.route('/investors', methods=['POST'])
def create_investor():
    try:
        investor_data = InvestorSchema(**request.json)

        existing_email = db.session.query(exists().where(Investor.email == investor_data.email)).scalar()

        if existing_email:
            return jsonify({'message': 'email already exists'}), 400

        investor = investor_factory(investor_data)

        return jsonify(investor.to_dict()), 200

    except ValidationError as e:
        return jsonify({
            "error": e.errors()
        }), 400

