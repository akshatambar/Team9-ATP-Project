from mysql.connector.errors import IntegrityError
from database import con, cursor, init_db, seed_discounts
from cart import print_table, view_cart, add_to_cart, remove_from_cart
from checkout import checkout, view_orders


# handles user login and new account signup
def login():
    while True:
        print("--- Options ---")
        print("1. Login\n2. Signup\n3. Exit")
        ch = input("Choice: ").strip()

        if ch == "1":
            m = input("Mobile: ").strip()
            if len(m) != 10 or not m.isdigit():
                print("Please enter a valid 10-digit mobile number.")
                continue
            cursor.execute("SELECT user_id, name FROM users WHERE mobile=%s", (m,))
            row = cursor.fetchone()
            if row:
                print(f"Welcome {row[1]}!\n")
                return row[0]
            else:
                print("Account not found!\n")

        elif ch == "2":
            n = input("Name: ").strip()
            m = input("Mobile: ").strip()
            a = input("Address: ").strip()
            if not n or not a or len(m) != 10 or not m.isdigit():
                print("Invalid input! Ensure name/address are filled and mobile is 10 digits.\n")
                continue
            try:
                cursor.execute("INSERT INTO users (name, mobile, address) VALUES (%s, %s, %s)", (n, m, a))
                con.commit()
                print(f"Signed up successfully! Welcome {n}!\n")
                return cursor.lastrowid
            except IntegrityError:
                print("Mobile number already exists!\n")

        elif ch == "3":
            exit()
        else:
            print("Invalid choice.\n")


# displays a restaurant's menu and lets the user manage their cart or checkout
def restaurant_menu(uid, rid, name):
    cursor.execute("SELECT item_id, item_name, description, rating, price FROM menu_items WHERE restaurant_id=%s", (rid,))
    print(f"\n--- Menu of {name} ---")
    print_table(cursor.fetchall(), ["ID", "Item", "Description", "Rating", "Price"])

    while True:
        print("--- Options ---")
        print("1. Add\n2. Remove\n3. View Cart\n4. Checkout\n5. View Orders\n6. Back")
        ch = input("Choice: ").strip()

        if ch == "1":
            ids_input = input("Enter Item ID(s) separated by comma: ")
            add_to_cart(uid, ids_input, rid)
        elif ch == "2":
            remove_from_cart(uid)
        elif ch == "3":
            view_cart(uid)
        elif ch == "4":
            checkout(uid, rid)
        elif ch == "5":
            view_orders(uid)
        elif ch == "6":
            break
        else:
            print("Invalid choice.")


# main loop that sets up the app, logs the user in, and shows restaurants
def main():
    print("Welcome to TROPHIX - Online Food Ordering System\n")
    init_db()
    seed_discounts()
    uid = login()

    while True:
        cursor.execute("SELECT restaurant_id, name, cuisine, rating FROM restaurants")
        rows = cursor.fetchall()
        print("--- Restaurants ---")
        print_table(rows, ["ID", "Name", "Cuisine", "Rating"])

        choice = input("Enter Restaurant ID or Name (or 'exit' to quit): ").strip()
        if choice.lower() == "exit":
            break

        if choice.isdigit():
            rid_int = int(choice)
            matched = [row for row in rows if row[0] == rid_int]
            if matched:
                restaurant_menu(uid, matched[0][0], matched[0][1])
            else:
                print("Invalid restaurant ID!")
        else:
            matched = [row for row in rows if choice.lower() in row[1].lower()]
            if matched:
                restaurant_menu(uid, matched[0][0], matched[0][1])
            else:
                print("No matching restaurant found!")


if __name__ == "__main__":
    main()