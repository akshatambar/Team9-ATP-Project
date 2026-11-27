from database import con, cursor


# prints rows neatly aligned as a table in the terminal
def print_table(rows, headers):
    if not rows:
        print("\nNo data available.\n")
        return

    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    header_line = " | ".join(str(headers[i]).ljust(widths[i]) for i in range(len(headers)))
    print("\n" + header_line)
    print("-" * len(header_line))

    for row in rows:
        print(" | ".join(str(row[i]).ljust(widths[i]) for i in range(len(row))))
    print()


# fetches and displays all items currently in the user's cart
def view_cart(uid):
    cursor.execute("""
        SELECT c.item_id, m.item_name, c.quantity, m.price, ROUND(c.quantity * m.price, 2)
        FROM cart c JOIN menu_items m ON c.item_id = m.item_id
        WHERE c.user_id = %s
    """, (uid,))
    rows = cursor.fetchall()
    if not rows:
        print("\nYour cart is empty!\n")
        return []

    table_data = [(r[0], r[1], r[2], f"Rs.{r[3]}", f"Rs.{r[4]}") for r in rows]
    print("\n--- Your Cart ---")
    print_table(table_data, ["ID", "Name", "Qty", "Price", "Total"])
    return rows


# adds one or more selected items to the cart, or updates quantity if already added
def add_to_cart(uid, iid_input, rid):
    item_ids = [i.strip() for i in iid_input.split(",") if i.strip().isdigit()]
    if not item_ids:
        print("Invalid Item ID(s).")
        return

    for iid in item_ids:
        cursor.execute("SELECT item_name FROM menu_items WHERE restaurant_id=%s AND item_id=%s", (rid, iid))
        row = cursor.fetchone()
        if row:
            qty = input(f"Enter quantity for {row[0]}: ").strip()
            if qty.isdigit() and int(qty) > 0:
                cursor.execute("SELECT quantity FROM cart WHERE user_id=%s AND item_id=%s", (uid, iid))
                if cursor.fetchone():
                    cursor.execute("UPDATE cart SET quantity=%s WHERE user_id=%s AND item_id=%s", (int(qty), uid, iid))
                else:
                    cursor.execute("INSERT INTO cart (user_id, item_id, quantity) VALUES (%s, %s, %s)", (uid, iid, int(qty)))
                con.commit()
                print(f"{qty} x {row[0]} added to cart!")
            else:
                print(f"Invalid quantity for Item {iid}, skipped.")
        else:
            print(f"Item ID {iid} not found in this restaurant!")


# deletes a chosen item from the user's cart
def remove_from_cart(uid):
    iid = input("Enter Item ID to remove: ").strip()
    if not iid.isdigit():
        print("Invalid Item ID.")
        return
    cursor.execute("DELETE FROM cart WHERE user_id=%s AND item_id=%s", (uid, int(iid)))
    con.commit()
    print("Item removed.")