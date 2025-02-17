from sqlalchemy import exists
from src.models.exchange_rate import ExchangeRate
from src.models.currency import Currency
from datetime import date, timedelta


def test_create_exchange_rate_route(client, session):
    test_currency = {'name': 'teste', 'type': 'TST'}
    currency = Currency(
            name=test_currency['name'],
            type=test_currency['type']
    )
    session.add(currency)
    session.commit()

    test_exchange_rate = {
        'date': '2025-02-15',
        'daily_variation': 1.2,
        'daily_rate': 1.5,
        'currency_id': currency.id
    }

    create_exchange_rate_response = client.post('/exchange-rates', json=test_exchange_rate)
    assert create_exchange_rate_response.status_code == 200

    created_exchange_rate_data = create_exchange_rate_response.json
    assert 'id' in created_exchange_rate_data
    assert created_exchange_rate_data['date'] == test_exchange_rate['date']
    assert created_exchange_rate_data['daily_variation'] == test_exchange_rate['daily_variation']
    assert created_exchange_rate_data['daily_rate'] == test_exchange_rate['daily_rate']
    assert created_exchange_rate_data['currency_name'] == currency.name
    assert created_exchange_rate_data['currency_type'] == currency.type

    created_exchange_rate_from_db = session.get(ExchangeRate, created_exchange_rate_data['id'])

    assert created_exchange_rate_from_db is not None
    assert created_exchange_rate_from_db.to_dict()['date'] == test_exchange_rate['date']
    assert created_exchange_rate_from_db.daily_variation == test_exchange_rate['daily_variation']
    assert created_exchange_rate_from_db.daily_rate == test_exchange_rate['daily_rate']
    assert created_exchange_rate_from_db.currency.name == currency.name
    assert created_exchange_rate_from_db.currency.type == currency.type


def test_create_exchange_rate_route_with_invalid_date(client, session):
    test_exchange_rate = {
        'date': '20250215',
        'daily_variation': 1.2,
        'daily_rate': 1.5,
        'currency_id': 1
    }

    create_exchange_rate_response = client.post('/exchange-rates', json=test_exchange_rate)
    assert create_exchange_rate_response.status_code == 400
    assert 'error' in create_exchange_rate_response.json


def test_create_exchange_rate_route_without_body(client):
    create_exchange_rate_response = client.post('/exchange-rates', json={})

    assert create_exchange_rate_response.status_code == 400
    assert 'error' in create_exchange_rate_response.json


def test_create_exchange_rate_with_invalid_currency_id(client, session):
    test_exchange_rate = {
        'date': '2025-02-15',
        'daily_variation': 1.2,
        'daily_rate': 1.5,
        'currency_id': 99
    }

    create_exchange_rate_response = client.post('/exchange-rates', json=test_exchange_rate)
    assert create_exchange_rate_response.status_code == 404

    create_exchange_rate_data = create_exchange_rate_response.json
    assert 'error' in create_exchange_rate_data
    assert create_exchange_rate_data['error'] in 'Currency id does not exist'


def test_get_recent_exchange_rate_route(client, session):
    currency = Currency(name='teste', type='TST')
    session.add(currency)
    session.commit()

    old_date = date.today() - timedelta(days=31)
    recent_date = date.today()

    old_exchange_rate = ExchangeRate(
        date=old_date,
        daily_variation=2.2,
        daily_rate=2.5,
        currency_id=currency.id
    )
    recent_exchange_rate = ExchangeRate(
        date=recent_date,
        daily_variation=1.2,
        daily_rate=1.5,
        currency_id=currency.id
    )

    session.add_all([old_exchange_rate, recent_exchange_rate])
    session.commit()

    get_recent_exchange_rate_response = client.get('/exchange-rates/recent')
    assert get_recent_exchange_rate_response.status_code == 200

    recent_exchange_rate_data = get_recent_exchange_rate_response.json

    assert isinstance(recent_exchange_rate_data, list)
    assert len(recent_exchange_rate_data) == 1

    fetched_recent_exchange_rate = recent_exchange_rate_data[0]

    assert fetched_recent_exchange_rate['id'] == recent_exchange_rate.id
    assert fetched_recent_exchange_rate['date'] == recent_exchange_rate.to_dict()['date']
    assert fetched_recent_exchange_rate['daily_rate'] == recent_exchange_rate.daily_rate
    assert fetched_recent_exchange_rate['daily_variation'] == recent_exchange_rate.daily_variation
    assert fetched_recent_exchange_rate['currency_name'] == recent_exchange_rate.currency.name
    assert fetched_recent_exchange_rate['currency_type'] == recent_exchange_rate.currency.type


def test_update_exchange_rate_route(client, session):
    currency = Currency(name='test', type='TST')

    session.add(currency)
    session.commit()

    created_exchange_rate = ExchangeRate(
        date=date(2025, 2, 15),
        daily_variation=1.2,
        daily_rate=1.5,
        currency_id=currency.id
    )

    session.add(created_exchange_rate)
    session.commit()

    updated_exchange_rate_payload = {
        'date': '2025-01-01',
        'daily_variation': 1.7,
        'daily_rate': 2.0,
    }

    update_exchange_rate_response = client.patch(f'/exchange-rates/{created_exchange_rate.id}',
                                                 json=updated_exchange_rate_payload)
    assert update_exchange_rate_response.status_code == 200

    updated_exchange_rate_data = update_exchange_rate_response.json
    assert updated_exchange_rate_data['id'] == created_exchange_rate.id
    assert updated_exchange_rate_data['date'] == updated_exchange_rate_payload['date']
    assert updated_exchange_rate_data['daily_variation'] == updated_exchange_rate_payload['daily_variation']
    assert updated_exchange_rate_data['daily_rate'] == updated_exchange_rate_payload['daily_rate']

    exchange_data_from_db = session.get(ExchangeRate, updated_exchange_rate_data['id'])

    assert exchange_data_from_db is not None
    assert exchange_data_from_db.to_dict()['date'] == updated_exchange_rate_payload['date']
    assert exchange_data_from_db.daily_variation == updated_exchange_rate_payload['daily_variation']
    assert exchange_data_from_db.daily_rate == updated_exchange_rate_payload['daily_rate']


def test_delete_old_exchange_rates_route(client, session):
    currency = Currency(name='teste', type='TST')
    session.add(currency)
    session.commit()

    old_date = date.today() - timedelta(days=31)
    created_old_exchange_rate = ExchangeRate(
        date=old_date,
        daily_variation=1.4,
        daily_rate=1.5,
        currency_id=currency.id
    )
    session.add(created_old_exchange_rate)
    session.commit()

    old_exchange_rate_id: int = created_old_exchange_rate.id

    delete_old_exchange_rates_response = client.delete(f'/exchange-rates/old')
    assert delete_old_exchange_rates_response.status_code == 200

    delete_old_exchange_rates_data = delete_old_exchange_rates_response.json
    assert 'message' in delete_old_exchange_rates_data
    assert delete_old_exchange_rates_data['message'] == '1 exchange rates older than 30 days were deleted'

    is_exchange_rate_deleted = not session.query(exists().where(ExchangeRate.id == old_exchange_rate_id)).scalar()

    assert is_exchange_rate_deleted
