import mysql.connector

# connect to mysql and select the project database
con = mysql.connector.connect(host="localhost", user="root", password="root")
cursor = con.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS project")
cursor.execute("USE project")


# creates all required tables and adds restaurant + menu data
def init_db():
    for tbl in ["orders", "cart", "discounts"]:
        cursor.execute(f"DROP TABLE IF EXISTS {tbl}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100), location VARCHAR(100),
            cuisine VARCHAR(50), delivery_time INT, rating DECIMAL(3,1)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            restaurant_id INT, item_name VARCHAR(100),
            price DECIMAL(8,2), description VARCHAR(255), rating DECIMAL(3,1),
            FOREIGN KEY(restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100), mobile VARCHAR(15) UNIQUE, address VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS discounts (
            discount_id INT AUTO_INCREMENT PRIMARY KEY,
            description VARCHAR(255), min_order DECIMAL(8,2),
            pct_off DECIMAL(5,2), max_off DECIMAL(8,2) NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            user_id INT, item_id INT, quantity INT,
            PRIMARY KEY(user_id, item_id),
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY(item_id) REFERENCES menu_items(item_id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT, restaurant VARCHAR(100),
            total_amt DECIMAL(8,2), discount_amt DECIMAL(8,2),
            final_amt DECIMAL(8,2), order_time DATETIME, delivery_time INT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    restaurants = [
        ("Murugan Idli Restaurant", "Mylapore", "South Indian", 30, 4.5),
        ("Ratna Cafe", "Triplicane", "South Indian", 25, 4.3),
        ("Sangeetha Adyar", "Adyar", "South Indian", 35, 4.4),
        ("Junior Kuppana", "T. Nagar", "Chettinad", 40, 4.2),
        ("Dominos", "Royapettah", "Pizza", 20, 4.0),
        ("McDonalds", "Nungambakkam", "Fast Food", 15, 3.9),
        ("Hotel Saravana Bhavan", "Mylapore", "South Indian", 30, 4.6),
        ("Paradise Biriyani", "Velachery", "Hyderabadi", 45, 4.3),
        ("Food Nirvana", "Besant Nagar", "Fusion", 50, 4.1),
        ("Creame Centre", "Alwarpet", "North Indian", 35, 4.2),
        ("Little Italy", "Nungambakkam", "Italian", 40, 4.4)
    ]

    menu_data = {
        "Murugan Idli Restaurant": [
            ("Podi Idli", 60, "Soft idlis coated with spicy lentil powder", 4.6),
            ("Garlic Podi Idli", 65, "Idli with garlic-infused podi", 4.5),
            ("Millet Pongal", 70, "Pongal made with millets and ghee", 4.4),
            ("Masala Dosai", 90, "Crispy dosa with potato masala", 4.5),
            ("Rava Dosai", 85, "Semolina-based crispy dosa", 4.3),
            ("Onion Uttapam", 80, "Thick dosa topped with onions", 4.4),
            ("Ghee Pongal", 75, "Creamy rice-lentil dish with ghee", 4.6),
            ("Mini Idli", 60, "Bite-sized idlis served with sambar", 4.5),
            ("Veg Biryani", 110, "Mildly spiced biryani with vegetables", 4.2),
            ("Parotta", 50, "Flaky layered bread", 4.3),
            ("Meals", 130, "South Indian thali with rice, sambar, rasam etc.", 4.6),
            ("Filter Coffee", 40, "Traditional South Indian coffee", 4.7),
            ("Jigarthanda", 90, "Chilled milk-based dessert drink", 4.5),
            ("Karupatti Halwa", 70, "Palm jaggery-based halwa", 4.4),
            ("Medhu Vada", 45, "Crispy lentil fritters", 4.5)
        ],
        "Ratna Cafe": [
            ("Sambar Idly", 80, "Idlis soaked in signature sambar", 4.7),
            ("Ghee Podi Dosa", 130, "Dosa with ghee and spicy podi", 4.5),
            ("Mysore Masala Dosa", 140, "Spicy chutney spread inside masala dosa", 4.6),
            ("Onion Rava Dosa", 120, "Crispy rava dosa with onion", 4.4),
            ("Paneer Butter Masala", 260, "Rich tomato-based paneer curry", 4.5),
            ("Channa Masala", 250, "Chickpeas in spicy gravy", 4.4),
            ("Mini Meals", 160, "Combo of rice, curry, and sides", 4.6),
            ("Veg Biryani", 130, "Aromatic rice with vegetables", 4.3),
            ("Rasmalai", 65, "Soft paneer balls in sweet milk", 4.5),
            ("Gulab Jamun", 55, "Deep-fried milk balls in syrup", 4.6),
            ("Filter Coffee", 50, "Strong South Indian coffee", 4.7),
            ("Ghee Pongal", 84, "Creamy pongal with ghee", 4.5),
            ("Medhu Vada", 49, "Crispy urad dal fritters", 4.4),
            ("Tomato Rice", 80, "Tangy tomato-flavored rice", 4.3),
            ("Curd Rice", 75, "Rice mixed with curd and spices", 4.4)
        ],
        "Sangeetha Adyar": [
            ("Masala Dosai", 130, "Dosa stuffed with spiced potato", 4.5),
            ("Ghee Roast", 170, "Crispy dosa roasted in ghee", 4.6),
            ("Rava Dosai", 115, "Semolina-based dosa", 4.4),
            ("Curd Vadai", 80, "Vada soaked in curd", 4.5),
            ("Pav Bhaji", 120, "Spicy mashed vegetables with buns", 4.4),
            ("Tomato Soup", 90, "Classic tomato soup", 4.3),
            ("South Indian Meals", 180, "Full thali with rice, sambar, rasam, etc.", 4.6),
            ("Vada Curry", 110, "Crumbled vada in spicy gravy", 4.5),
            ("Sweet Lime Juice", 190, "Fresh lime juice", 4.4),
            ("Filter Coffee", 65, "Strong decoction coffee", 4.7),
            ("Onion Bajji", 65, "Onion fritters", 4.3),
            ("Chilli Parotta", 130, "Spicy stir-fried parotta", 4.4),
            ("Paneer Butter Masala", 240, "Creamy paneer curry", 4.5),
            ("Kashmiri Naan", 95, "Sweet naan with dry fruits", 4.4),
            ("Carrot Halwa", 110, "Sweet dessert made with grated carrot", 4.6)
        ],
        "Junior Kuppana": [
            ("Chicken Biryani", 180, "Spicy Chettinad-style biryani", 4.6),
            ("Mutton Chukka", 220, "Dry-fried mutton with spices", 4.5),
            ("Egg Podimas", 90, "Scrambled eggs with curry leaves", 4.4),
            ("Parotta", 60, "Flaky layered bread", 4.3),
            ("Chicken 65", 150, "Deep-fried spicy chicken", 4.5),
            ("Fish Fry", 200, "Seer fish fried with masala", 4.4),
            ("Mutton Biryani", 220, "Rich biryani with tender mutton", 4.6),
            ("Kari Dosa", 130, "Dosa topped with minced meat", 4.5),
            ("Chicken Curry", 160, "Traditional Chettinad chicken curry", 4.4),
            ("Onion Raita", 40, "Yogurt with onions", 4.2),
            ("Veg Meals", 140, "Rice with veg curries and sides", 4.3),
            ("Butter Chicken", 180, "Creamy tomato-based chicken curry", 4.4),
            ("Egg Dosa", 90, "Dosa with egg topping", 4.3),
            ("Mutton Kola", 150, "Spicy mutton balls", 4.5),
            ("Ghee Rice", 100, "Rice cooked with ghee and spices", 4.2)
        ],
        "Dominos": [
            ("Margherita Pizza", 149, "Classic cheese pizza", 4.2),
            ("Farmhouse Pizza", 299, "Veggies like capsicum, onion, tomato, mushroom", 4.3),
            ("Peppy Paneer", 319, "Paneer with spicy toppings", 4.4),
            ("Veg Extravaganza", 349, "Loaded with exotic veggies", 4.5),
            ("Cheese Burst Pizza", 399, "Extra cheese-filled crust", 4.6),
            ("Garlic Breadsticks", 129, "Soft bread with garlic flavor", 4.4),
            ("Stuffed Garlic Bread", 159, "Garlic bread with cheese stuffing", 4.5),
            ("Choco Lava Cake", 99, "Molten chocolate dessert", 4.6),
            ("Tandoori Paneer Pizza", 329, "Paneer with tandoori spices", 4.3),
            ("Mexican Green Wave", 299, "Spicy Mexican-style pizza", 4.2),
            ("Indi Tandoori Chicken", 349, "Chicken with Indian spices", 4.4),
            ("Chicken Pepperoni", 369, "Classic pepperoni pizza", 4.5),
            ("Paneer Makhani Pizza", 319, "Paneer with makhani sauce", 4.3),
            ("Classic Veg Pizza", 199, "Simple veggie pizza", 4.1),
            ("Coke (500ml)", 60, "Chilled soft drink", 4.0)
        ],
        "McDonalds": [
            ("McAloo Tikki Burger", 59, "Spiced potato patty burger", 4.2),
            ("McVeggie Burger", 89, "Veg patty with lettuce and mayo", 4.3),
            ("McChicken Burger", 99, "Chicken patty with creamy mayo", 4.4),
            ("Chicken McNuggets (6 pcs)", 149, "Crispy chicken bites", 4.5),
            ("Fries (Medium)", 89, "Golden crispy fries", 4.6),
            ("Veg Pizza McPuff", 45, "Veg pizza filling in puff pastry", 4.4),
            ("Chocolate Shake", 129, "Thick chocolate milkshake", 4.5),
            ("Strawberry Shake", 129, "Strawberry flavored shake", 4.4),
            ("Coke Float", 99, "Coke with vanilla ice cream", 4.3),
            ("McFlurry Oreo", 129, "Vanilla ice cream with Oreo", 4.6),
            ("Spicy Paneer Wrap", 149, "Paneer wrap with spicy sauce", 4.3),
            ("Chicken Maharaja Mac", 199, "Double chicken patty burger", 4.4),
            ("Veg Maharaja Mac", 189, "Double veg patty burger", 4.2),
            ("Iced Tea", 79, "Refreshing lemon iced tea", 4.1),
            ("Hot Coffee", 69, "Fresh brewed coffee", 4.2)
        ],
        "Hotel Saravana Bhavan": [
            ("Mini Tiffin", 120, "Combo of idli, dosa, pongal, vada", 4.6),
            ("Ghee Roast Dosa", 140, "Crispy dosa roasted in ghee", 4.5),
            ("Onion Rava Dosa", 130, "Semolina dosa with onions", 4.4),
            ("Sambar Vada", 90, "Vada soaked in sambar", 4.5),
            ("Vegetable Kurma", 110, "Mixed vegetables in coconut gravy", 4.4),
            ("Poori Masala", 100, "Fluffy poori with potato masala", 4.3),
            ("South Indian Meals", 180, "Thali with rice, sambar, rasam, etc.", 4.6),
            ("Tomato Soup", 80, "Classic tomato soup", 4.2),
            ("Paneer Butter Masala", 240, "Creamy paneer curry", 4.5),
            ("Butter Naan", 90, "Soft naan with butter", 4.4),
            ("Carrot Halwa", 110, "Sweet carrot dessert", 4.6),
            ("Filter Coffee", 50, "Strong South Indian coffee", 4.7),
            ("Rasam", 40, "Spicy tamarind soup", 4.3),
            ("Curd Rice", 80, "Rice mixed with curd", 4.4),
            ("Medhu Vada", 60, "Crispy urad dal fritters", 4.5)
        ],
        "Paradise Biriyani": [
            ("Chicken Biriyani", 220, "Hyderabadi-style chicken biriyani", 4.6),
            ("Mutton Biriyani", 260, "Tender mutton biriyani", 4.5),
            ("Veg Biriyani", 180, "Aromatic vegetable biriyani", 4.4),
            ("Paneer Tikka", 200, "Grilled paneer cubes", 4.5),
            ("Chicken 65", 160, "Spicy deep-fried chicken", 4.4),
            ("Egg Curry", 140, "Boiled eggs in spicy gravy", 4.3),
            ("Raita", 40, "Yogurt with onions and spices", 4.2),
            ("Gulab Jamun", 60, "Milk balls in sugar syrup", 4.5),
            ("Double Ka Meetha", 90, "Hyderabadi bread pudding", 4.6),
            ("Tandoori Chicken", 240, "Grilled chicken with spices", 4.5),
            ("Butter Naan", 80, "Soft naan with butter", 4.4),
            ("Chicken Kebab", 200, "Spicy grilled chicken", 4.5),
            ("Veg Korma", 160, "Mixed veg in creamy gravy", 4.3),
            ("Chicken Curry", 180, "Traditional spicy chicken curry", 4.4),
            ("Soft Drink", 50, "Chilled beverage", 4.0)
        ],
        "Food Nirvana": [
            ("Thai Green Curry", 240, "Spicy coconut-based Thai curry", 4.5),
            ("Burmese Khow Suey", 260, "Noodles in coconut curry", 4.6),
            ("Fusion Nachos", 180, "Nachos with Indian toppings", 4.4),
            ("Paneer Tikka Quesadilla", 220, "Indian-Mexican fusion wrap", 4.5),
            ("Peri Peri Fries", 120, "Fries with spicy peri peri seasoning", 4.3),
            ("Masala Pasta", 200, "Pasta with Indian spices", 4.4),
            ("Tandoori Pizza", 250, "Pizza with tandoori toppings", 4.5),
            ("Chilli Cheese Toast", 150, "Spicy cheesy toast", 4.3),
            ("Veg Sushi Roll", 180, "Fusion sushi with Indian flavors", 4.2),
            ("Mocktail Nirvana", 130, "Signature fruit mocktail", 4.4),
            ("Chocolate Mousse", 160, "Rich chocolate dessert", 4.6),
            ("Paneer Wrap", 190, "Grilled paneer wrap", 4.4),
            ("Loaded Nachos", 200, "Nachos with cheese and beans", 4.5),
            ("Veg Burger", 150, "Burger with Indian-style patty", 4.3),
            ("Cold Coffee", 120, "Chilled coffee drink", 4.4)
        ],
        "Creame Centre": [
            ("Chole Bhature", 220, "Spicy chickpeas with fried bread", 4.6),
            ("Sizzling Brownie", 180, "Brownie with hot chocolate sauce", 4.5),
            ("Nachos Grande", 200, "Loaded nachos with cheese", 4.4),
            ("Italian Sizzler", 280, "Grilled veggies and pasta", 4.5),
            ("Paneer Tikka", 240, "Grilled paneer cubes", 4.4),
            ("Veg Sizzler", 260, "Hot plate of grilled veggies", 4.5),
            ("Mac n Cheese", 220, "Creamy cheesy pasta", 4.4),
            ("Cold Coffee", 120, "Chilled coffee drink", 4.3),
            ("Tandoori Platter", 300, "Assorted grilled items", 4.5),
            ("Hakka Noodles", 180, "Stir-fried noodles with veggies", 4.3),
            ("Spring Rolls", 160, "Crispy rolls with veg filling", 4.4),
            ("Veg Manchurian", 190, "Fried veg balls in spicy sauce", 4.5),
            ("Cheese Corn Balls", 170, "Fried balls with cheese and corn", 4.4),
            ("Fruit Punch", 130, "Mixed fruit mocktail", 4.3)
        ],
        "Little Italy": [
            ("Bruschetta", 180, "Toasted bread with tomato and basil", 4.5),
            ("Pasta Alfredo", 260, "Creamy white sauce pasta", 4.6),
            ("Pasta Arrabiata", 250, "Spicy tomato sauce pasta", 4.4),
            ("Margherita Pizza", 300, "Classic tomato and cheese pizza", 4.5),
            ("Quattro Formaggi Pizza", 360, "Four cheese pizza", 4.6),
            ("Risotto Funghi", 280, "Creamy mushroom risotto", 4.5),
            ("Lasagna", 320, "Layered pasta with cheese and sauce", 4.4),
            ("Tiramisu", 200, "Coffee-flavored Italian dessert", 4.6),
            ("Garlic Bread", 150, "Toasted bread with garlic butter", 4.3),
            ("Zuppa di Verdure", 160, "Italian vegetable soup", 4.4),
            ("Panacotta", 190, "Creamy dessert with berry sauce", 4.5),
            ("Pizza Verde", 310, "Pizza with green veggies", 4.4),
            ("Cannelloni", 330, "Stuffed pasta tubes in sauce", 4.5),
            ("Mocktail Italiano", 140, "Signature Italian mocktail", 4.3),
            ("Espresso", 120, "Strong Italian coffee", 4.4)
        ]
    }

    cursor.execute("SELECT COUNT(*) FROM restaurants")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO restaurants (name, location, cuisine, delivery_time, rating) VALUES (%s, %s, %s, %s, %s)",
            restaurants
        )
        con.commit()

    cursor.execute("SELECT restaurant_id, name FROM restaurants")
    restaurant_ids = {name: rid for rid, name in cursor.fetchall()}

    cursor.execute("SELECT COUNT(*) FROM menu_items")
    if cursor.fetchone()[0] == 0:
        for name, items in menu_data.items():
            rid = restaurant_ids[name]
            for item_name, price, desc, rating in items:
                cursor.execute(
                    "INSERT INTO menu_items (restaurant_id, item_name, price, description, rating) VALUES (%s, %s, %s, %s, %s)",
                    (rid, item_name, price, desc, rating)
                )
        con.commit()


# adds default discount offers into the database
def seed_discounts():
    cursor.execute("SELECT COUNT(*) FROM discounts")
    if cursor.fetchone()[0] == 0:
        defaults = [
            ("50% off up to Rs.100 on orders above Rs.500", 500, 50, 100),
            ("25% off up to Rs.75 on orders above Rs.200", 200, 25, 75),
            ("20% off up to Rs.150 on orders above Rs.400", 400, 20, 150),
            ("10% off up to Rs.35 on orders above Rs.100", 100, 10, 35),
            ("5% off on all orders", 0, 5, None)
        ]
        cursor.executemany(
            "INSERT INTO discounts (description, min_order, pct_off, max_off) VALUES (%s, %s, %s, %s)",
            defaults
        )
        con.commit()