#!/usr/bin/env python3
from flask import Flask, request, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

def convert_currency(from_currency, to_currency):
    try:
        url = f'https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get('success'):
            return {
                'rate': data['info']['rate'],
                'from': from_currency,
                'to': to_currency,
                'date': data['date'],
                'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            return {'error': f"Conversion error: {data.get('error', 'Unknown error')}"}

    except Exception as e:
        return {'error': str(e)}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Currency Converter</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 20px auto; padding: 20px; }
        .container { background-color: #f0f0f0; border-radius: 5px; padding: 20px; }
        .rate { font-size: 22px; font-weight: bold; margin: 10px 0; }
        .info { font-size: 14px; color: gray; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Currency Converter</h2>
        <form method="get" action="/convert">
            <label>From Currency: <input type="text" name="from" value="{{ from_currency or '' }}" required></label><br><br>
            <label>To Currency: <input type="text" name="to" value="{{ to_currency or '' }}" required></label><br><br>
            <button type="submit">Convert</button>
        </form>
        <hr>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% elif rate %}
            <p class="rate">1 {{ from_currency }} = {{ rate }} {{ to_currency }}</p>
            <p class="info">Date: {{ date }} | Local Time: {{ current_time }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/convert', methods=['GET'])
def convert():
    from_currency = request.args.get('from', '').upper()
    to_currency = request.args.get('to', '').upper()

    if not from_currency or not to_currency:
        return render_template_string(HTML_TEMPLATE, error="Please provide both 'from' and 'to' currencies.")

    result = convert_currency(from_currency, to_currency)
    return render_template_string(HTML_TEMPLATE, **result, from_currency=from_currency, to_currency=to_currency)

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("Currency converter running at http://127.0.0.1:5000/convert")
    app.run(debug=True, host='0.0.0.0', port=5000)
