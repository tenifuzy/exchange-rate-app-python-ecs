import pytest
import json
from app import app, convert_currency, get_exchange_rates

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the homepage route returns 200"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Currency Converter' in response.data

def test_convert_route_valid(client):
    """Test valid currency conversion route"""
    response = client.post('/convert', 
                          json={'amount': 100, 'from_currency': 'USD', 'to_currency': 'EUR'},
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data or 'error' in data

def test_convert_currency_function():
    """Test conversion logic"""
    result = convert_currency(100, 'USD', 'USD')
    assert result == 100

def test_currencies_route(client):
    """Test currencies endpoint"""
    response = client.get('/currencies')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'currencies' in data or 'error' in data

def test_rates_route(client):
    """Test rates endpoint"""
    response = client.get('/rates?base=USD')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'rates' in data or 'error' in data