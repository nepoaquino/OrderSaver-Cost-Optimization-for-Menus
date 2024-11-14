from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.common.exceptions import TimeoutException  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import time
import csv
import os

# List of URLs for each category
urls = [
    'https://www.jollibeedelivery.com/menu/new-products',
    'https://www.jollibeedelivery.com/menu/family-meals',
    'https://www.jollibeedelivery.com/menu/breakfast',
    'https://www.jollibeedelivery.com/menu/chickenjoy',
    'https://www.jollibeedelivery.com/menu/chicken-nuggets',
    'https://www.jollibeedelivery.com/menu/burgers',
    'https://www.jollibeedelivery.com/menu/jolly-spaghetti',
    'https://www.jollibeedelivery.com/menu/burger-steak',
    'https://www.jollibeedelivery.com/menu/super-meals-main-category',
    'https://www.jollibeedelivery.com/menu/chicken-sandwich',
    'https://www.jollibeedelivery.com/menu/jolly-hotdog-and-pies-main-category',
    'https://www.jollibeedelivery.com/menu/palabok-main-category',
    'https://www.jollibeedelivery.com/menu/fries-and-sides',
    'https://www.jollibeedelivery.com/menu/mc-desserts',
    'https://www.jollibeedelivery.com/menu/beverages',
    'https://www.jollibeedelivery.com/menu/jollibee-kids-meal'
]

# Set up the WebDriver (make sure to have the ChromeDriver executable in your PATH)
driver = webdriver.Chrome()

# Open a CSV file for writing
current_directory = os.getcwd()  # Get the current working directory
file_name = 'products_menu.csv'
file_path = os.path.join(current_directory, file_name)

with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)

    # Loop through each URL to scrape data
    for url in urls:
        driver.get(url)

        # Wait for the product container to be present (adjust the locator as needed)
        try:
            # Increase the wait time to ensure the content is fully loaded
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'column.category-menu__menu-item'))
            )
            # Add a short delay to ensure all data is fully loaded
            time.sleep(5)
        except TimeoutException:  # type: ignore
            print(f"Timeout waiting for {url}")
            continue

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract the category name from the URL (this will be used as the key)
        category_name = url.split('/')[-1].replace('-', ' ').title()

        # Initialize a list to store the extracted products for this category
        products = []

        # Extract all product containers (divs with class 'column category-menu__menu-item')
        product_divs = soup.find_all('div', class_='column category-menu__menu-item')

        # Loop through each product div and extract item name and price
        for product_div in product_divs:
            # Extract the item name from the h2 tag inside the current div
            item_name_tag = product_div.find('h2', {'data-test-id': 'ItemSelector'})
            item_name = item_name_tag.text.strip() if item_name_tag else "Item name not found"

            # Clean up item_name to remove any double quotes
            item_name = item_name.replace('"', '')  # Remove double quotes

            # Extract the price from the span tag with class 'amount'
            price_tag = product_div.find('span', class_='amount')
            price = f"{price_tag.text.strip()}" if price_tag else "Price not found"

            # Add the cleaned item name and price to the products list
            products.append({"item_name": item_name, "price": price})

        # Write the category data to the CSV with a comment above each section
        writer.writerow([f"# {category_name}"])
        writer.writerow(['item_name', 'price'])  # Write the header row for this category

        # Write the data rows for this category
        for product in products:
            writer.writerow([product['item_name'], product['price']])

        # Add a blank row to separate categories
        writer.writerow([])

    print(f"Data saved to {file_name}")

# Quit the driver
driver.quit()
