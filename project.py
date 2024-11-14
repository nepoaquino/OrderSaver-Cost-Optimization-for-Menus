from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import json
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

# Dictionary to store the data by category
category_data = {}

# Loop through each URL to scrape data
for url in urls:
    driver.get(url)

    # Wait for the product container to be present (adjust the locator as needed)
    try:
        # Wait for the page to load completely by looking for a product container element
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'column.category-menu__menu-item'))
        )
    except TimeoutException:
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
        if item_name_tag:
            item_name = item_name_tag.text.strip()
        else:
            item_name = "Item name not found"

        # Extract the price from the span tag with class 'amount' inside the current div
        price_tag = product_div.find('span', class_='amount')
        if price_tag:
            price = f"₱ {price_tag.text.strip()}"
        else:
            price = "Price not found"

        # Add the item name and price to the products list
        products.append({"item_name": item_name, "price": price})

    # Store the products list in the dictionary under the category name
    category_data[category_name] = products

    # Save the CSV file in the current working directory
    current_directory = os.getcwd()  # Get the current working directory
    file_name = f'{category_name.replace(" ", "_")}_menu.csv'
    file_path = os.path.join(current_directory, file_name)

    # Write the category's data to a CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['item_name', 'price']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        for product in products:
            writer.writerow(product)

# Quit the driver
driver.quit()

# Output the results as a JSON file (for example)
json_file_path = os.path.join(current_directory, 'menu_data.json')
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(category_data, json_file, ensure_ascii=False, indent=4)

# Optionally, print the results to the console for verification
print(json.dumps(category_data, ensure_ascii=False, indent=4))
