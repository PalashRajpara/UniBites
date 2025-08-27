import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import time

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ---------- Models ----------

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    image_url = db.Column(db.String(200), default='placeholder.jpg')
    image_path = db.Column(db.String(200), default='placeholder.jpg')
    is_available = db.Column(db.Boolean, default=True)

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

# ---------- User loader for Flask-Login ----------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- Routes ----------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists", "danger")
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('menu'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('index'))

@app.route('/menu')
def menu():
    categories = Category.query.order_by(Category.id).all()
    for category in categories:
        category.products = Product.query.filter_by(category_id=category.id, is_available=True).all()
    return render_template('menu.html', categories=categories)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = request.form.get('quantity', 1, type=int)
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash("Item added to cart successfully!", "success")
    return redirect(url_for('menu'))

@app.route('/cart')
@login_required
def cart():
    cart_items = db.session.query(Cart, Product).join(Product, Cart.product_id == Product.id).filter(Cart.user_id == current_user.id).all()
    total = sum(item.Cart.quantity * item.Product.price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/cart/update/<int:cart_id>', methods=['POST'])
@login_required
def update_cart(cart_id):
    action = request.form.get('action')
    cart_item = Cart.query.get_or_404(cart_id)
    
    if cart_item.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('cart'))
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
            flash("Item removed from cart.", "info")
            db.session.commit()
            return redirect(url_for('cart'))
    
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    
    if cart_item.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash("Item removed from cart.", "success")
    return redirect(url_for('cart'))

@app.route('/orders')
@login_required
def orders():
    # Fetch orders for current_user from DB - placeholder example
    # orders = Order.query.filter_by(user_id=current_user.id).all()
    # For now, show an empty page or dummy message
    orders = []
    return render_template('orders.html', orders=orders)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/checkout')
@login_required
def checkout():
    # Get cart items and calculate total
    cart_items = db.session.query(Cart, Product).join(Product, Cart.product_id == Product.id)\
        .filter(Cart.user_id == current_user.id).all()
    
    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect(url_for('cart'))
    
    total = sum(item.Cart.quantity * item.Product.price for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/process-payment', methods=['POST'])
@login_required
def process_payment():
    # Mock payment processing - always succeeds after 2 seconds
    time.sleep(2)  # Simulate payment processing delay
    
    # Clear user's cart after "successful" payment
    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    
    flash("Payment successful! Your order has been placed.", "success")
    return redirect(url_for('payment_success'))

@app.route('/payment-success')
@login_required
def payment_success():
    return render_template('payment_success.html')

# ---------- Database setup routes (optional) ----------

@app.route('/admin/setup')
def setup_database():
    categories = ["Main Dishes", "Snacks", "Beverages", "Desserts"]
    
    for cat_name in categories:
        if not Category.query.filter_by(name=cat_name).first():
            category = Category(name=cat_name)
            db.session.add(category)
    
    db.session.commit()
    return "Categories created successfully!"

@app.route('/admin/add_products')
def add_sample_products():
    main_dishes = Category.query.filter_by(name="Main Dishes").first().id
    snacks = Category.query.filter_by(name="Snacks").first().id
    beverages = Category.query.filter_by(name="Beverages").first().id
    desserts = Category.query.filter_by(name="Desserts").first().id

    products = [
        # Main Dishes
        Product(name="Margherita Pizza", description="Fresh mozzarella, tomato sauce, and basil leaves", price=399.00, category_id=main_dishes, image_path="MainDishes/pizza_margherita.jpg"),
        Product(name="Vegetable Pasta", description="Creamy alfredo sauce with mixed vegetables", price=299.00, category_id=main_dishes, image_path="MainDishes/pasta_alfredo.jpg"),
        Product(name="Vegetable Fried Rice", description="Aromatic basmati rice with mixed vegetables", price=249.00, category_id=main_dishes, image_path="MainDishes/rice_fried.jpg"),
        Product(name="Vegetable Hakka Noodles", description="Stir-fried noodles with fresh vegetables", price=219.00, category_id=main_dishes, image_path="MainDishes/noodles_hakka.jpg"),
        Product(name="Paneer Wrap", description="Grilled paneer with fresh vegetables in a tortilla", price=179.00, category_id=main_dishes, image_path="MainDishes/wrap_paneer.jpg"),
        Product(name="Cheese Quesadilla", description="Melted cheese in a crispy tortilla", price=229.00, category_id=main_dishes, image_path="MainDishes/quesadilla_cheese.jpg"),
        Product(name="Veggie Burger", description="Plant-based patty with fresh vegetables", price=189.00, category_id=main_dishes, image_path="MainDishes/burger_veggie.jpg"),
        Product(name="Grilled Cheese Sandwich", description="Golden grilled sandwich with melted cheese", price=159.00, category_id=main_dishes, image_path="MainDishes/sandwich_cheese.jpg"),
        
        # Snacks
        Product(name="French Fries", description="Crispy golden potato fries", price=99.00, category_id=snacks, image_path="Snacks/fries_regular.jpg"),
        Product(name="Loaded Nachos", description="Tortilla chips with cheese and toppings", price=149.00, category_id=snacks, image_path="Snacks/nachos_loaded.jpg"),
        Product(name="Vegetable Samosa", description="Crispy pastry filled with spiced vegetables", price=49.00, category_id=snacks, image_path="Snacks/samosa_veg.jpg"),
        Product(name="Onion Pakora", description="Deep-fried onion fritters", price=79.00, category_id=snacks, image_path="Snacks/pakora_onion.jpg"),
        Product(name="Vegetable Spring Rolls", description="Crispy rolls filled with fresh vegetables", price=119.00, category_id=snacks, image_path="Snacks/roll_spring.jpg"),
        Product(name="Potato Wedges", description="Seasoned potato wedges", price=109.00, category_id=snacks, image_path="Snacks/wedges_potato.jpg"),
        Product(name="Cheese Sticks", description="Fried mozzarella sticks", price=129.00, category_id=snacks, image_path="Snacks/sticks_cheese.jpg"),
        
        # Beverages
        Product(name="Latte", description="Espresso with steamed milk", price=89.00, category_id=beverages, image_path="Beverages/coffee_latte.jpg"),
        Product(name="Masala Chai", description="Traditional Indian spiced tea", price=39.00, category_id=beverages, image_path="Beverages/tea_masala.jpg"),
        Product(name="Fresh Orange Juice", description="Freshly squeezed orange juice", price=69.00, category_id=beverages, image_path="Beverages/juice_orange.jpg"),
        Product(name="Mango Smoothie", description="Creamy mango smoothie", price=99.00, category_id=beverages, image_path="Beverages/smoothie_mango.jpg"),
        Product(name="Cola", description="Chilled cola", price=49.00, category_id=beverages, image_path="Beverages/soda_cola.jpg"),
        Product(name="Bottled Water", description="Pure drinking water", price=29.00, category_id=beverages, image_path="Beverages/water_bottle.jpg"),
        Product(name="Iced Tea", description="Refreshing iced tea", price=59.00, category_id=beverages, image_path="Beverages/tea_iced.jpg"),
        
        # Desserts
        Product(name="Chocolate Cake", description="Rich chocolate cake slice", price=149.00, category_id=desserts, image_path="Desserts/cake_chocolate.jpg"),
        Product(name="Vanilla Ice Cream", description="Creamy vanilla ice cream", price=79.00, category_id=desserts, image_path="Desserts/icecream_vanilla.jpg"),
        Product(name="Chocolate Chip Cookie", description="Homemade chocolate chip cookie", price=39.00, category_id=desserts, image_path="Desserts/cookie_chocolate.jpg"),
        Product(name="Fudge Brownie", description="Decadent chocolate brownie", price=119.00, category_id=desserts, image_path="Desserts/brownie_fudge.jpg"),
        Product(name="Strawberry Ice Cream", description="Fresh strawberry ice cream", price=89.00, category_id=desserts, image_path="Desserts/icecream_strawberry.jpg"),
    ]

    for product in products:
        if not Product.query.filter_by(name=product.name).first():
            db.session.add(product)
    
    db.session.commit()
    return f"Added {len(products)} vegetarian products successfully!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create the database
    app.run(debug=True)

# Main Dishes:
# 	•	`pizza_margherita.jpg` - Margherita Pizza
# 	•	`pasta_alfredo.jpg` - Vegetable Pasta
# 	•	`rice_fried.jpg` - Vegetable Fried Rice
# 	•	`noodles_hakka.jpg` - Vegetable Hakka Noodles
# 	•	`wrap_paneer.jpg` - Paneer Wrap
# 	•	`quesadilla_cheese.jpg` - Cheese Quesadilla
# 	•	`burger_veggie.jpg` - Veggie Burger
# 	•	`sandwich_cheese.jpg` - Grilled Cheese Sandwich
# Snacks:
# 	•	`fries_regular.jpg` - French Fries
# 	•	`nachos_loaded.jpg` - Loaded Nachos
# 	•	`samosa_veg.jpg` - Vegetable Samosa
# 	•	`pakora_onion.jpg` - Onion Pakora
# 	•	`roll_spring.jpg` - Vegetable Spring Rolls
# 	•	`wedges_potato.jpg` - Potato Wedges
# 	•	`sticks_cheese.jpg` - Cheese Sticks
# Beverages: (same as before)
# 	•	`coffee_latte.jpg` - Latte
# 	•	`tea_masala.jpg` - Masala Chai
# 	•	`juice_orange.jpg` - Fresh Orange Juice
# 	•	`smoothie_mango.jpg` - Mango Smoothie
# 	•	`soda_cola.jpg` - Cola
# 	•	`water_bottle.jpg` - Bottled Water
# 	•	`tea_iced.jpg` - Iced Tea
# Desserts: (same as before)
# 	•	`cake_chocolate.jpg` - Chocolate Cake
# 	•	`icecream_vanilla.jpg` - Vanilla Ice Cream
# 	•	`cookie_chocolate.jpg` - Chocolate Chip Cookie
# 	•	`brownie_fudge.jpg` - Fudge Brownie
# 	•	`icecream_strawberry.jpg` - Strawberry Ice Cream
