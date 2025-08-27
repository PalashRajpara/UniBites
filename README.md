# UniBites - Canteen Food Ordering System

UniBites is a modern, user-friendly web application designed to streamline the food ordering process in university canteens. Built with Flask and featuring a responsive design, UniBites offers a seamless experience for students and staff to order food from their campus canteen.

## 🚀 Features

### For Customers
- **User Authentication**
  - Secure registration and login system
  - Password encryption for user safety
  - Profile management

- **Menu Navigation**
  - Browse items by categories
  - View detailed product descriptions
  - See prices
  - High-quality food images

- **Shopping Cart**
  - Add/remove items
  - Adjust quantities
  - Real-time price updates
  - Persistent cart across sessions

- **Ordering**
  - Streamlined checkout process
  - Order history tracking

### Menu Categories
1. **Main Dishes** 🍽️
   - Margherita Pizza
   - Vegetable Pasta
   - Vegetable Fried Rice
   - Vegetable Hakka Noodles
   - Paneer Wrap
   - Cheese Quesadilla
   - Veggie Burger
   - Grilled Cheese Sandwich

2. **Snacks** 🍟
   - French Fries
   - Loaded Nachos
   - Vegetable Samosa
   - Onion Pakora
   - Vegetable Spring Rolls
   - Potato Wedges
   - Cheese Sticks

3. **Beverages** 🥤
   - Latte
   - Masala Chai
   - Fresh Orange Juice
   - Mango Smoothie
   - Cola
   - Bottled Water
   - Iced Tea

4. **Desserts** 🍰
   - Chocolate Cake
   - Vanilla Ice Cream
   - Chocolate Chip Cookie
   - Fudge Brownie
   - Strawberry Ice Cream

## 💻 Technology Stack

- **Backend Framework**: Flask (Python)
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Frontend**: 
  - HTML5, CSS3, JavaScript
  - Bootstrap for responsive design
- **Security**:
  - Password Hashing
  - CSRF Protection
  - Secure Session Management

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/UniBites.git
cd UniBites
```

2. Create a virtual environment and activate it:
```bash
python -m venv unibites_env
source unibites_env/bin/activate  # On Windows: unibites_env\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file with following variables
DATABASE_URL=mysql://username:password@localhost/unibites
SECRET_KEY=your_secret_key
```

5. Initialize the database:
```bash
flask run
# Visit http://localhost:5000/admin/setup to set up categories
# Visit http://localhost:5000/admin/add_products to add sample products
```

## 🚀 Usage

1. Start the application:
```bash
flask run
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## 📱 Screenshots

1. Register
<img width="3420" height="1890" alt="1" src="https://github.com/user-attachments/assets/dda66da0-5f33-4514-b10d-c0af5287a809" />

2. Login
<img width="3420" height="1890" alt="2" src="https://github.com/user-attachments/assets/571b5ca4-1e16-44a9-9ce4-d63013b6274c" />

3. Home
<img width="3420" height="1890" alt="3" src="https://github.com/user-attachments/assets/f11d48a2-6e0d-4a41-aadd-d499ba998b09" />

4. Menu
<img width="3420" height="1892" alt="4" src="https://github.com/user-attachments/assets/0529acbc-bd77-43bb-9767-60715b72108f" />

5. Cart
<img width="3412" height="1874" alt="5" src="https://github.com/user-attachments/assets/a52fdb8e-53af-4cb6-9bce-632a8c4a61cc" />

## 🔒 Security Features

- Secure password hashing using Werkzeug
- CSRF protection for forms
- Session-based authentication
- Protected routes with login requirements
- Input validation and sanitization

## 🎨 Design Features

- Responsive design for all devices
- Intuitive user interface
- Consistent orange theme (#FF5F1F)
- Modern and clean layout
- Optimized images
- Loading animations
- Toast notifications

## ⚡ Performance Optimizations

- Efficient database queries
- Image optimization
- Responsive image loading
- Minimized CSS and JavaScript
- Browser caching support

## 🔄 Future Enhancements

- [ ] Real-time order tracking
- [ ] Push notifications
- [ ] Rating and review system
- [ ] Loyalty points system
- [ ] Multiple payment gateway integration
- [ ] Admin dashboard
- [ ] Analytics and reporting
- [ ] Mobile app version

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## 📧 Contact

For any queries or support, please contact:
Linkedin : Palash Rajpara

---
Made with ❤️ for University Students
# UniBites
