from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

def get_exchange_rates(base_currency='USD'):
    """
    Get exchange rates from a free API without requiring an API key
    """
    try:
        # Using exchangerate-api.com free tier (no API key required)
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return None

def convert_currency(amount, from_currency, to_currency):
    """
    Convert currency using free exchange rate API
    """
    try:
        # Get exchange rates with base currency as 'from_currency'
        rates_data = get_exchange_rates(from_currency)
        
        if rates_data and 'rates' in rates_data:
            rates = rates_data['rates']
            
            # If converting to the same currency
            if from_currency == to_currency:
                return amount
            
            # Get the rate for target currency
            if to_currency in rates:
                rate = rates[to_currency]
                converted_amount = amount * rate
                return round(converted_amount, 2)
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error converting currency: {e}")
        return None

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teniola's Currency Converter App</title>
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
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 500px;
            animation: fadeIn 0.5s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
            font-size: 1.1em;
        }

        input, select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e1e1;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: #f9f9f9;
        }

        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .currency-row {
            display: flex;
            gap: 15px;
            align-items: end;
        }

        .currency-group {
            flex: 1;
        }

        .swap-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            margin-bottom: 5px;
        }

        .swap-btn:hover {
            transform: rotate(180deg);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        .convert-btn {
            width: 100%;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 18px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
        }

        .convert-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }

        .convert-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }

        .result {
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
            border-radius: 15px;
            text-align: center;
            color: white;
            font-size: 18px;
            font-weight: 600;
            display: none;
            animation: slideIn 0.5s ease-in;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .result.show {
            display: block;
        }

        .error {
            background: linear-gradient(45deg, #ff6b6b, #ee5a52);
        }

        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .rate-info {
            margin-top: 15px;
            padding: 15px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            font-size: 14px;
        }

        @media (max-width: 600px) {
            .container {
                padding: 20px;
            }
            
            .currency-row {
                flex-direction: column;
                gap: 10px;
            }
            
            .swap-btn {
                align-self: center;
                transform: rotate(90deg);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💱 Teniola's Currency Converter App</h1>
        
        <form id="converterForm">
            <div class="form-group">
                <label for="amount">Amount</label>
                <input type="number" id="amount" step="0.01" min="0.01" placeholder="Enter amount" required>
            </div>

            <div class="currency-row">
                <div class="currency-group">
                    <label for="fromCurrency">From</label>
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

                <button type="button" class="swap-btn" id="swapBtn" title="Swap currencies">⇄</button>

                <div class="currency-group">
                    <label for="toCurrency">To</label>
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
                // Clear existing options except the first one
                [this.fromSelect, this.toSelect].forEach(select => {
                    while (select.children.length > 1) {
                        select.removeChild(select.lastChild);
                    }
                });

                // Add currency options
                currencies.forEach(currency => {
                    const option1 = new Option(currency, currency);
                    const option2 = new Option(currency, currency);
                    this.fromSelect.add(option1);
                    this.toSelect.add(option2);
                });

                // Set default values
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

        // Initialize the converter when the page loads
        document.addEventListener('DOMContentLoaded', () => {
            new CurrencyConverter();
        });
    </script>
</body>
</html>'''

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
    """
    Get list of available currencies
    """
    try:
        rates_data = get_exchange_rates('USD')
        if rates_data and 'rates' in rates_data:
            currencies = list(rates_data['rates'].keys())
            currencies.append('USD')  # Add base currency
            currencies.sort()
            return jsonify({'currencies': currencies})
        else:
            return jsonify({'error': 'Could not fetch currencies'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rates')
def get_rates():
    """
    Get current exchange rates
    """
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
    # Run the Flask web server when executed as a script
    print("Starting web server. Access the exchange rate at http://127.0.0.1:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)
