from flask import Flask, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for flash messages

# Example inventory with stock counts
inventory = {
    'Vitamin C Serum': {'stock': 10},
    'Hydrating Moisturizer': {'stock': 15},
    'Sunscreen SPF 50': {'stock': 5},
}

# Simple purchase log list storing purchase events as dicts
purchase_log = []

@app.route('/')
def index():
    return render_template('index.html', inventory=inventory)

# Fix: add <product> as URL parameter here!
@app.route('/purchase/<product>')
def purchase(product):
    if product in inventory and inventory[product]['stock'] > 0:
        # Reduce stock by 1
        inventory[product]['stock'] -= 1

        # Add purchase event with timestamp (string for simplicity)
        from datetime import datetime
        purchase_log.append({
            'product': product,
            'quantity': 1,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        flash(f'Successfully purchased 1 {product}.', 'success')

        # Optional: alert if stock low
        if inventory[product]['stock'] <= 3:
            flash(f'Warning: Low stock for {product}. Consider restocking!', 'warning')
    else:
        flash(f'Cannot purchase {product}. Out of stock or invalid.', 'error')

    return redirect(url_for('index'))

@app.route('/log')
def show_log():
    # Render the purchase log page using log.html template
    return render_template('log.html', purchase_log=purchase_log)

if __name__ == '__main__':
    app.run(debug=True)
