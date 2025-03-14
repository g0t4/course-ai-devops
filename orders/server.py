from flask import Flask, jsonify
import random
import math

app = Flask(__name__)

def fake_heavy_computation():
    num = random.randint(80_000, 130_000)
    _ = math.factorial(num) 
    return True

@app.route('/order')
def process_order():
    fake_heavy_computation()
    return jsonify({"status": "Order processed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
