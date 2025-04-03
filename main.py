from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

TOYYIB_SECRET_KEY = os.getenv("TOYYIB_SECRET_KEY", "l0f6cyv6-tv47-hdlz-xqas-to1o6j1amh6v")
TOYYIB_CATEGORY_CODE = os.getenv("TOYYIB_CATEGORY_CODE", "gnuga7m4")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/create-invoice', methods=['POST'])
def create_invoice():
    data = request.json
    user_id = data.get("user_id")
    package = data.get("package")
    amount = data.get("amount")

    payload = {
        'userSecretKey': TOYYIB_SECRET_KEY,
        'categoryCode': TOYYIB_CATEGORY_CODE,
        'billName': f"{package} Package",
        'billDescription': f'{package} subscription for Telegram ID {user_id}',
        'billPriceSetting': 1,
        'billPayorInfo': 1,
        'billAmount': str(amount * 100),  # RM to sen
        'billReturnUrl': 'https://telegram.me/pablocollectbot',
        'billCallbackUrl': '',
        'billExternalReferenceNo': f"{user_id}-{package}",
        'billTo': f'TelegramUser{user_id}',
        'billEmail': f'{user_id}@mail.com',
        'billPhone': '0123456789',
        'billSplitPayment': 0
    }

    resp = requests.post('https://dev.toyyibpay.com/index.php/api/createBill', data=payload)
    try:
        bill_code = resp.json()[0]['BillCode']
        url = f'https://toyyibpay.com/{bill_code}'
        return jsonify({"url": url})
    except Exception:
        return jsonify({"error": "Failed to create bill"}), 500

if __name__ == '__main__':
    app.run(debug=True)
