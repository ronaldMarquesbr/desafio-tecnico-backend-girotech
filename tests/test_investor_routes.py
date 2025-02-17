from src.models.investor import Investor
from src.models.investment_history import InvestmentHistory
from src.models.currency import Currency


def test_create_investor_route(client, session):
    test_investor = {'name': 'Ronald', 'email': 'ronald@email.com'}
    create_investor_response = client.post('/investors', json=test_investor)
    assert create_investor_response.status_code == 200

    create_investor_data = create_investor_response.json
    assert 'id' in create_investor_data
    assert create_investor_data['name'] == test_investor['name']
    assert create_investor_data['email'] == test_investor['email']

    created_investor = session.get(Investor, create_investor_data['id'])

    assert created_investor is not None
    assert created_investor.id == create_investor_data['id']
    assert created_investor.name == test_investor['name']
    assert created_investor.email == test_investor['email']


def test_create_investor_route_without_body(client):
    create_investor_response = client.post('/investors', json={})

    assert create_investor_response.status_code == 400
    assert 'error' in create_investor_response.json


def test_create_investor_route_with_repeated_email(client, session):
    test_investor = {'name': 'ronald', 'email': 'ronald@email.com'}
    session.add(
        Investor(
            name=test_investor['name'],
            email=test_investor['email']
        )
    )
    session.commit()

    create_investor_response = client.post('/investors', json=test_investor)
    assert create_investor_response.status_code == 400

    create_investor_data = create_investor_response.json
    assert 'message' in create_investor_data
    assert create_investor_data['message'] == 'email already exists'


def test_delete_investor_route(client, session):
    currency = Currency(name='test', type='TST')
    investor = Investor(name='Ronald', email='ronald@email.com')
    session.add_all([currency, investor])
    session.commit()

    investor_id = investor.id

    investment_history = InvestmentHistory(
        initial_amount=1000,
        months=2,
        interest_rate=1.1,
        final_amount=1200,
        currency_id=currency.id,
        investor_id=investor.id
    )

    session.add(investment_history)
    session.commit()

    delete_investor_response = client.delete(f'/investor/{investor.id}')
    assert delete_investor_response.status_code == 200

    delete_investor_data = delete_investor_response.json
    assert 'message' in delete_investor_data
    assert delete_investor_data['message'] == 'Investor deleted successfully'

    is_investor_deleted = Investor.query.filter_by(id=investor_id).scalar() is None
    has_deleted_investments = InvestmentHistory.query.filter_by(investor_id=investor_id).scalar() is None

    assert is_investor_deleted
    assert has_deleted_investments


def test_delete_investor_with_invalid_id(client):
    delete_investor_response = client.delete('/investor/99')
    assert delete_investor_response.status_code == 404

    delete_investor_data = delete_investor_response.json
    assert 'error' in delete_investor_data
    assert delete_investor_data['error'] == 'Investor not found'
