from flask import Flask, jsonify, redirect, url_for
import random
import math
import datetime
import uuid

app = Flask(__name__)

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

    def fake_heavy_computation():
        num = random.randint(80_000, 130_000)
        _ = math.factorial(num)
        return True

    fake_heavy_computation()
    
    order_id = str(uuid.uuid4())
    products = ["Widget", "Gadget", "Doohickey", "Thingamajig"]
    order_items = []
    
    num_items = random.randint(1, 3)
    order_total = 0
    
    for _ in range(num_items):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        price = round(random.uniform(9.99, 49.99), 2)
        item_total = round(quantity * price, 2)
        order_total += item_total
        
        order_items.append({
            "product": product,
            "quantity": quantity,
            "price": price,
            "total": item_total
        })
    
    timestamp = datetime.datetime.now().isoformat()
    
    delivery_days = random.randint(3, 7)
    delivery_date = (datetime.datetime.now() + datetime.timedelta(days=delivery_days)).strftime("%Y-%m-%d")
    
    response = {
        "status": "Order processed",
        "order_id": order_id,
        "timestamp": timestamp,
        "items": order_items,
        "order_total": round(order_total, 2),
        "shipping": {
            "method": random.choice(["Standard", "Express", "Next Day"]),
            "estimated_delivery": delivery_date
        },
        "payment": {
            "method": random.choice(["Credit Card", "PayPal", "Apple Pay"]),
            "status": "Completed"
        }
    }
    
    return jsonify(response), 200

@app.errorhandler(404)
def page_not_found(_):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
