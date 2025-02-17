from src.models.investment_history import InvestmentHistory
from src.models.currency import Currency
from src.models.investor import Investor


def test_create_investment_history_route(client, session):
    currency = Currency(name='test', type='TST')
    investor = Investor(name='Ronald', email='ronald@email.com')

    session.add_all([currency, investor])
    session.commit()

    test_investment_history = {
        'initial_amount': 1000,
        'months': 2,
        'interest_rate': 1.1,
        'final_amount': 1200,
        'currency_id': currency.id,
        'investor_id': investor.id
    }

    create_investment_response = client.post('/investments', json=test_investment_history)
    assert create_investment_response.status_code == 200

    create_investment_data = create_investment_response.json
    assert create_investment_data['initial_amount'] == test_investment_history['initial_amount']
    assert create_investment_data['months'] == test_investment_history['months']
    assert create_investment_data['interest_rate'] == test_investment_history['interest_rate']
    assert create_investment_data['final_amount'] == test_investment_history['final_amount']
    assert create_investment_data['currency_id'] == test_investment_history['currency_id']
    assert create_investment_data['investor_id'] == test_investment_history['investor_id']


def test_create_investment_with_invalid_currency_id(client, session):
    investor = Investor(name='Ronald', email='ronald@email.com')
    session.add(investor)
    session.commit()

    test_investment_history = {
        'initial_amount': 1000,
        'months': 2,
        'interest_rate': 1.1,
        'final_amount': 1200,
        'currency_id': 99,
        'investor_id': investor.id
    }

    create_investment_response = client.post('/investments', json=test_investment_history)
    assert create_investment_response.status_code == 404
    assert 'error' in create_investment_response.json
    assert create_investment_response.json['error'] == 'Currency id does not exist'


def test_create_investment_with_invalid_investor_id(client, session):
    currency = Currency(name='teste', type='TST')
    session.add(currency)
    session.commit()

    test_investment_history = {
        'initial_amount': 1000,
        'months': 2,
        'interest_rate': 1.1,
        'final_amount': 1200,
        'currency_id': currency.id,
        'investor_id': 99
    }

    create_investment_response = client.post('/investments', json=test_investment_history)
    assert create_investment_response.status_code == 404
    assert 'error' in create_investment_response.json
    assert create_investment_response.json['error'] == 'Investor id does not exist'


def test_create_investment_history_route_without_body(client):
    create_investment_response = client.post('/investments', json={})

    assert create_investment_response.status_code == 400
    assert 'error' in create_investment_response.json
