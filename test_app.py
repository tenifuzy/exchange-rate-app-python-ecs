import pytest
from app import app, convert_currency

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
    response = client.get('/convert?from=USD&to=EUR')
    assert response.status_code == 200
    assert b'USD' in response.data and b'EUR' in response.data

def test_convert_currency_function_valid():
    """Test conversion logic for valid currency pair"""
    result = convert_currency('USD', 'NGN')
    assert isinstance(result, dict)
    assert 'rate' in result
    assert result['rate'] > 0

def test_convert_currency_function_invalid():
    """Test conversion logic with invalid currency"""
    result = convert_currency('XXX', 'ZZZ')
    assert isinstance(result, dict)
    assert 'error' in result

def test_convert_route_missing_params(client):
    """Test /convert without parameters"""
    response = client.get('/convert')
    assert response.status_code == 200
    assert b'Please provide both' in response.data
