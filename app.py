from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from datetime import datetime
import smtplib
from email.mime.text import MimeText

app = Flask(__name__)
CORS(app)

orders = []
products = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    return jsonify(products)

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create new order"""
    try:
        order_data = request.get_json()
        
        # Validate required fields
        required_fields = ['items', 'customer_info', 'total']
        for field in required_fields:
            if field not in order_data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Create order object
        order = {
            'id': len(orders) + 1,
            'items': order_data['items'],
            'customer_info': order_data['customer_info'],
            'total': order_data['total'],
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'order_number': f'HT{datetime.now().strftime("%Y%m%d")}{len(orders) + 1:04d}'
        }
        
        orders.append(order)
        
        # Send confirmation email (in production)
        # send_order_confirmation(order)
        
        return jsonify({
            'success': True,
            'order_id': order['id'],
            'order_number': order['order_number']
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order by ID"""
    order = next((o for o in orders if o['id'] == order_id), None)
    if order:
        return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

@app.route('/api/contact', methods=['POST'])
def contact_form():
    """Handle contact form submissions"""
    try:
        contact_data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if field not in contact_data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Here you would typically save to database and send email
        print(f"Contact form submission: {contact_data}")
        
        return jsonify({'success': True, 'message': 'Message sent successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_order_confirmation(order):
    """Send order confirmation email (placeholder function)"""
    # This would be implemented with your email service
    print(f"Sending confirmation for order {order['order_number']}")
    pass

if __name__ == '__main__':
    # Load sample products
    with open('products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    app.run(debug=True, port=5000)