from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skincare_inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    current_stock = db.Column(db.Integer, default=0)
    min_stock_level = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    purchases = db.relationship('Purchase', backref='product', lazy=True)
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.min_stock_level
    
    @property
    def total_value(self):
        return self.current_stock * self.price

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost_per_unit = db.Column(db.Float, nullable=False)
    supplier = db.Column(db.String(100), nullable=False)
    purchase_date = db.Column(db.Date, default=date.today)
    notes = db.Column(db.Text)
    
    @property
    def total_cost(self):
        return self.quantity * self.cost_per_unit

# Routes
@app.route('/')
def dashboard():
    total_products = Product.query.count()
    low_stock_products = Product.query.filter(Product.current_stock <= Product.min_stock_level).all()
    total_inventory_value = sum(p.total_value for p in Product.query.all())
    recent_purchases = Purchase.query.order_by(Purchase.purchase_date.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_products=total_products,
                         low_stock_count=len(low_stock_products),
                         low_stock_products=low_stock_products,
                         total_inventory_value=total_inventory_value,
                         recent_purchases=recent_purchases)

@app.route('/products')
def products():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Product.query
    
    if search:
        query = query.filter(Product.name.contains(search) | Product.brand.contains(search))
    
    if category:
        query = query.filter(Product.category == category)
    
    products = query.order_by(Product.name).all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('products.html', products=products, categories=categories, 
                         current_search=search, current_category=category)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            product = Product(
                name=request.form['name'],
                brand=request.form['brand'],
                category=request.form['category'],
                price=float(request.form['price']),
                current_stock=int(request.form['current_stock']),
                min_stock_level=int(request.form['min_stock_level'])
            )
            
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            flash(f'Error adding product: {str(e)}', 'error')
    
    return render_template('add_product.html')

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            product.name = request.form['name']
            product.brand = request.form['brand']
            product.category = request.form['category']
            product.price = float(request.form['price'])
            product.current_stock = int(request.form['current_stock'])
            product.min_stock_level = int(request.form['min_stock_level'])
            
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            flash(f'Error updating product: {str(e)}', 'error')
    
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'info')
    except Exception as e:
        flash(f'Error deleting product: {str(e)}', 'error')
    return redirect(url_for('products'))

@app.route('/purchases')
def purchases():
    page = request.args.get('page', 1, type=int)
    purchases = Purchase.query.order_by(Purchase.purchase_date.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('purchases.html', purchases=purchases)

@app.route('/add_purchase', methods=['GET', 'POST'])
def add_purchase():
    if request.method == 'POST':
        try:
            product_id = int(request.form['product_id'])
            quantity = int(request.form['quantity'])
            
            purchase = Purchase(
                product_id=product_id,
                quantity=quantity,
                cost_per_unit=float(request.form['cost_per_unit']),
                supplier=request.form['supplier'],
                purchase_date=datetime.strptime(request.form['purchase_date'], '%Y-%m-%d').date(),
                notes=request.form.get('notes', '')
            )
            
            # Update product stock
            product = Product.query.get(product_id)
            if product:
                product.current_stock += quantity
                
                db.session.add(purchase)
                db.session.commit()
                flash('Purchase recorded successfully!', 'success')
                return redirect(url_for('purchases'))
            else:
                flash('Product not found!', 'error')
        except Exception as e:
            flash(f'Error recording purchase: {str(e)}', 'error')
    
    products = Product.query.order_by(Product.name).all()
    return render_template('add_purchase.html', products=products, today=date.today())

@app.route('/low_stock')
def low_stock():
    products = Product.query.filter(Product.current_stock <= Product.min_stock_level).all()
    return render_template('low_stock.html', products=products)

@app.route('/api/stock_alerts')
def stock_alerts_api():
    products = Product.query.filter(Product.current_stock <= Product.min_stock_level).all()
    alerts = []
    for product in products:
        alerts.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'current_stock': product.current_stock,
            'min_stock_level': product.min_stock_level
        })
    return jsonify(alerts)

@app.route('/adjust_stock/<int:id>', methods=['POST'])
def adjust_stock(id):
    try:
        product = Product.query.get_or_404(id)
        adjustment = int(request.form['adjustment'])
        reason = request.form.get('reason', 'Manual adjustment')
        
        product.current_stock += adjustment
        if product.current_stock < 0:
            product.current_stock = 0
        
        db.session.commit()
        flash(f'Stock adjusted for {product.name}. Reason: {reason}', 'info')
    except Exception as e:
        flash(f'Error adjusting stock: {str(e)}', 'error')
    
    return redirect(url_for('products'))

# Initialize database
def create_tables():
    with app.app_context():
        db.create_all()
        
        # Add sample data if no products exist
        if Product.query.count() == 0:
            sample_products = [
                Product(name='Vitamin C Serum', brand='GlowSkin', category='Serums', price=45.99, current_stock=12, min_stock_level=5),
                Product(name='Hyaluronic Acid Moisturizer', brand='HydraLux', category='Moisturizers', price=32.50, current_stock=3, min_stock_level=8),
                Product(name='Gentle Foaming Cleanser', brand='PureCleanse', category='Cleansers', price=24.99, current_stock=15, min_stock_level=6),
                Product(name='Retinol Night Cream', brand='YouthRenew', category='Treatments', price=67.00, current_stock=2, min_stock_level=4),
                Product(name='SPF 30 Daily Sunscreen', brand='SunGuard', category='Sunscreens', price=28.75, current_stock=8, min_stock_level=10)
            ]
            
            for product in sample_products:
                db.session.add(product)
            
            try:
                db.session.commit()
                print("Sample data added successfully!")
            except Exception as e:
                print(f"Error adding sample data: {e}")
                db.session.rollback()

if __name__ == '__main__':
    create_tables()
    print("Starting Skincare Inventory App...")
    print("Access the app at: http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)