import sqlite3

def view_scraped_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('sephora_products.db')
    cursor = conn.cursor()

    # Fetch all rows from the 'products' table
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No data found.")
    else:
        print("Scraped Data:")
        for row in rows:
            print(f"Product ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Brand: {row[2]}")
            print(f"Price: {row[3]}")
            print(f"Ingredients: {row[4]}")
            print(f"Image URL: {row[5]}")
            print("---------------------------------------")

    # Close the connection to the database
    conn.close()

if __name__ == "__main__":
    view_scraped_data()