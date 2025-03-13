from flask import Flask, jsonify
import random
import math

app = Flask(__name__)

def fake_heavy_computation():
    """Pointless CPU-intensive work (simulating bad order processing)."""
    num = random.randint(50_000, 100_000)  # Large number for CPU strain
    _ = math.factorial(num)  # Expensive operation
    return True

@app.route('/order')
def process_order():
    """Fake order processing that maxes out the CPU."""
    fake_heavy_computation()
    return jsonify({"status": "Order processed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
