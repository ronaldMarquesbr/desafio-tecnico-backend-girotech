from src.models.currency import Currency


def test_create_currency_route(client, session):
    test_currency = {'name': 'Test', 'type': 'TST'}
    create_currency_response = client.post('/currencies', json=test_currency)
    assert create_currency_response.status_code == 200

    create_currency_data = create_currency_response.json
    assert 'id' in create_currency_data
    assert create_currency_data['name'] == test_currency['name']
    assert create_currency_data['type'] == test_currency['type']

    created_currency = session.get(Currency, create_currency_data['id'])
    assert created_currency is not None
    assert created_currency.id == create_currency_data['id']
    assert created_currency.name == test_currency['name']
    assert created_currency.type == test_currency['type']


def test_get_currencies(client, session):
    test_currency = Currency(name='Test', type='TST')
    session.add(test_currency)
    session.commit()

    get_currency_response = client.get('/currencies')
    assert get_currency_response.status_code == 200

    response_json = get_currency_response.get_json()
    assert isinstance(response_json, list)

    fetched_currency = response_json[0]

    assert fetched_currency['name'] == test_currency.name
    assert fetched_currency['type'] == test_currency.type
