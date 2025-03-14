from flask import Flask, jsonify, redirect, url_for
import random
import math

app = Flask(__name__)

def fake_heavy_computation():
    num = random.randint(80_000, 130_000)
    _ = math.factorial(num) 
    return True

@app.route('/')
def home():
    return '''
    <html>
        <body>
            <h1>Hello!</h1>
            <p>Place an order <a href="/order">here</a>.</p>
        </body>
    </html>
    '''

@app.route('/order')
def process_order():
    fake_heavy_computation()
    return jsonify({"status": "Order processed"}), 200

@app.errorhandler(404)
def page_not_found(e):
    # Redirect to home page for any unmapped routes
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
