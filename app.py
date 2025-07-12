import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

def get_exchange_rates(base_currency='USD'):
    """
    Fetch exchange rates from a free API
    """
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None

def convert_currency(amount, from_currency, to_currency):
    """
    Convert currency using exchange rates
    """
    if from_currency == to_currency:
        return amount
    
    rates_data = get_exchange_rates(from_currency)
    if rates_data and 'rates' in rates_data:
        if to_currency in rates_data['rates']:
            rate = rates_data['rates'][to_currency]
            return round(amount * rate, 2)
    return None

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currency Converter</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 500px;
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 2rem;
            font-size: 2rem;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            color: #555;
            font-weight: 600;
        }

        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }

        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }

        .currency-row {
            display: flex;
            gap: 1rem;
            align-items: end;
        }

        .currency-group {
            flex: 1;
        }

        .swap-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 18px;
            transition: background-color 0.3s ease;
            margin-bottom: 0;
        }

        .swap-btn:hover {
            background: #5a67d8;
        }

        .convert-btn {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
        }

        .convert-btn:hover {
            transform: translateY(-2px);
        }

        .convert-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .loading {
            display: none;
            text-align: center;
            margin: 2rem 0;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .result {
            margin-top: 2rem;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
        }

        .result.show {
            opacity: 1;
            transform: translateY(0);
            background: #f8f9fa;
            border: 2px solid #e9ecef;
        }

        .result.error {
            background: #f8d7da;
            border: 2px solid #f5c6cb;
            color: #721c24;
        }

        .rate-info {
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Currency Converter</h1>
        
        <form id="converterForm">
            <div class="form-group">
                <label for="amount">Amount:</label>
                <input type="number" id="amount" step="0.01" min="0.01" placeholder="Enter amount" required>
            </div>

            <div class="currency-row">
                <div class="currency-group">
                    <label for="fromCurrency">From:</label>
                    <select id="fromCurrency" required>
                        <option value="">Select currency</option>
                        <option value="USD">USD - US Dollar</option>
                        <option value="EUR">EUR - Euro</option>
                        <option value="GBP">GBP - British Pound</option>
                        <option value="JPY">JPY - Japanese Yen</option>
                        <option value="CAD">CAD - Canadian Dollar</option>
                        <option value="AUD">AUD - Australian Dollar</option>
                        <option value="CHF">CHF - Swiss Franc</option>
                        <option value="CNY">CNY - Chinese Yuan</option>
                        <option value="INR">INR - Indian Rupee</option>
                        <option value="BRL">BRL - Brazilian Real</option>
                    </select>
                </div>

                <button type="button" class="swap-btn" id="swapBtn">⇄</button>

                <div class="currency-group">
                    <label for="toCurrency">To:</label>
                    <select id="toCurrency" required>
                        <option value="">Select currency</option>
                        <option value="USD">USD - US Dollar</option>
                        <option value="EUR">EUR - Euro</option>
                        <option value="GBP">GBP - British Pound</option>
                        <option value="JPY">JPY - Japanese Yen</option>
                        <option value="CAD">CAD - Canadian Dollar</option>
                        <option value="AUD">AUD - Australian Dollar</option>
                        <option value="CHF">CHF - Swiss Franc</option>
                        <option value="CNY">CNY - Chinese Yuan</option>
                        <option value="INR">INR - Indian Rupee</option>
                        <option value="BRL">BRL - Brazilian Real</option>
                    </select>
                </div>
            </div>

            <button type="submit" class="convert-btn" id="convertBtn">Convert Currency</button>
        </form>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Converting...</p>
        </div>

        <div class="result" id="result"></div>
    </div>

    <script>
        class CurrencyConverter {
            constructor() {
                this.form = document.getElementById('converterForm');
                this.amountInput = document.getElementById('amount');
                this.fromSelect = document.getElementById('fromCurrency');
                this.toSelect = document.getElementById('toCurrency');
                this.swapBtn = document.getElementById('swapBtn');
                this.convertBtn = document.getElementById('convertBtn');
                this.loading = document.getElementById('loading');
                this.result = document.getElementById('result');
                
                this.init();
            }

            init() {
                this.form.addEventListener('submit', (e) => this.handleSubmit(e));
                this.swapBtn.addEventListener('click', () => this.swapCurrencies());
                this.loadCurrencies();
            }

            async loadCurrencies() {
                try {
                    const response = await fetch('/currencies');
                    const data = await response.json();
                    
                    if (data.currencies) {
                        this.populateCurrencySelects(data.currencies);
                    }
                } catch (error) {
                    console.error('Error loading currencies:', error);
                }
            }

            populateCurrencySelects(currencies) {
                [this.fromSelect, this.toSelect].forEach(select => {
                    while (select.children.length > 1) {
                        select.removeChild(select.lastChild);
                    }
                });

                currencies.forEach(currency => {
                    const option1 = new Option(currency, currency);
                    const option2 = new Option(currency, currency);
                    this.fromSelect.add(option1);
                    this.toSelect.add(option2);
                });

                this.fromSelect.value = 'USD';
                this.toSelect.value = 'EUR';
            }

            swapCurrencies() {
                const fromValue = this.fromSelect.value;
                const toValue = this.toSelect.value;
                
                this.fromSelect.value = toValue;
                this.toSelect.value = fromValue;
            }

            async handleSubmit(e) {
                e.preventDefault();
                
                const amount = parseFloat(this.amountInput.value);
                const fromCurrency = this.fromSelect.value;
                const toCurrency = this.toSelect.value;

                if (!amount || !fromCurrency || !toCurrency) {
                    this.showError('Please fill in all fields');
                    return;
                }

                this.showLoading();

                try {
                    const response = await fetch('/convert', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            amount: amount,
                            from_currency: fromCurrency,
                            to_currency: toCurrency
                        })
                    });

                    const data = await response.json();

                    if (response.ok && data.success) {
                        this.showResult(data);
                    } else {
                        this.showError(data.error || 'Conversion failed');
                    }
                } catch (error) {
                    this.showError('Network error. Please try again.');
                } finally {
                    this.hideLoading();
                }
            }

            showLoading() {
                this.loading.style.display = 'block';
                this.convertBtn.disabled = true;
                this.result.classList.remove('show');
            }

            hideLoading() {
                this.loading.style.display = 'none';
                this.convertBtn.disabled = false;
            }

            showResult(data) {
                this.result.className = 'result show';
                this.result.innerHTML = `
                    <div>
                        <strong>${data.original_amount} ${data.from_currency}</strong> = 
                        <strong>${data.converted_amount} ${data.to_currency}</strong>
                    </div>
                    <div class="rate-info">
                        Exchange Rate: 1 ${data.from_currency} = ${data.rate} ${data.to_currency}
                    </div>
                `;
            }

            showError(message) {
                this.result.className = 'result show error';
                this.result.innerHTML = `<strong>Error:</strong> ${message}`;
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            new CurrencyConverter();
        });
    </script>
</body>
</html>''')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        from_currency = data.get('from_currency', 'USD').upper()
        to_currency = data.get('to_currency', 'EUR').upper()
        
        if amount <= 0:
            return jsonify({'error': 'Amount must be greater than 0'}), 400
        
        converted_amount = convert_currency(amount, from_currency, to_currency)
        
        if converted_amount is not None:
            return jsonify({
                'success': True,
                'original_amount': amount,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'converted_amount': converted_amount,
                'rate': round(converted_amount / amount, 4)
            })
        else:
            return jsonify({'error': 'Currency conversion failed. Please check currency codes.'}), 400
            
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/currencies')
def get_currencies():
    try:
        rates_data = get_exchange_rates('USD')
        if rates_data and 'rates' in rates_data:
            currencies = list(rates_data['rates'].keys())
            currencies.append('USD')
            currencies.sort()
            return jsonify({'currencies': currencies})
        else:
            return jsonify({'error': 'Could not fetch currencies'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rates')
def get_rates():
    try:
        base_currency = request.args.get('base', 'USD').upper()
        rates_data = get_exchange_rates(base_currency)
        
        if rates_data:
            return jsonify(rates_data)
        else:
            return jsonify({'error': 'Could not fetch exchange rates'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)