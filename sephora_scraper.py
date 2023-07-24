import time
import random
import sqlite3
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions

def setup_database():
    # Connect to the SQLite database (creates one if not already present)
    conn = sqlite3.connect('sephora_products.db')

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Execute SQL to create the 'products' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            brand TEXT,
            price TEXT,
            ingredients TEXT,
            image_url TEXT
        )
    ''')

    # Commit the changes to the database (save the table structure)
    conn.commit()

    # Close the connection to the database
    conn.close()

def scrape_sephora_products():
    url = "https://www.sephora.com/shop/skincare"
    
    # Set up undetected-chromedriver options
    options = ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")  
    
    with Chrome(options=options) as driver:
        # Wait for the page to load 
        driver.get(url)
        time.sleep(5)  

        # Scroll down to load more products (can be changed)
        num_scrolls = 3
        for _ in range(num_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Random sleep to avoid pattern detection
            time.sleep(random.uniform(1, 3))  

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # All individual skincare products
        products_class1 = soup.find_all('div', class_='css-1qe8tjm')
        products_class2 = soup.find_all('div', class_='css-foh208')
        products = products_class1 + products_class2

        # Connect to the SQLite database
        conn = sqlite3.connect('sephora_products.db')
        cursor = conn.cursor()

        for product in products:
            try:
                # Extract product information from each product element
                name = product.find('span', class_='ProductTile-name css-h8cc3p eanm77i0').text.strip()
                brand = product.find('span', class_='css-12z2u5 eanm77i0').text.strip()
                price = product.find('span', class_='css-0').text.strip()
                ingredients = product.find('div', class_='css-1ue8dmw eanm77i0').text.strip()
                image_url = product.find('img')['src']

                # Insert the data into the database
                cursor.execute('INSERT INTO products (name, brand, price, ingredients, image_url) VALUES (?, ?, ?, ?, ?)',
                               (name, brand, price, ingredients, image_url))
            except Exception as e:
                print(f"Error extracting product information: {e}")

        # Commit the changes and close the connection to the database
        conn.commit()
        conn.close()
        print("Scraping and database insertion complete.")

if __name__ == "__main__":
    setup_database()
    scrape_sephora_products()