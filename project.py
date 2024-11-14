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
    'https://www.jollibeedelivery.com/menu/best-sellers',
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
    'https://www.jollibeedelivery.com/menu/jollibee-kids-meal',
    'https://www.jollibeedelivery.com/menu/meals-under-650-kcal-for-coke-stores'
]

# Set up the WebDriver (make sure to have the ChromeDriver executable in your PATH)
driver = webdriver.Chrome()

# Open a CSV file for writing
current_directory = os.getcwd()  # Get the current working directory
file_name = 'menu.csv'
file_path = os.path.join(current_directory, file_name)

# Use a set to store unique (item_name, price) pairs
unique_products = set()

with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['item_name', 'price'])  # Write the header row once

    for url in urls:
        print(f"\nScraping: {url}...")
        driver.get(url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'column.category-menu__menu-item'))
            )
            time.sleep(2)
        except TimeoutException:
            print(f"Timeout waiting for {url}")
            continue

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_divs = soup.find_all('div', class_='column category-menu__menu-item')

        for product_div in product_divs:
            # Extract the item name and price
            item_name_tag = product_div.find('h2', {'data-test-id': 'ItemSelector'})
            item_name = item_name_tag.text.strip() if item_name_tag else "Item name not found"
            price_tag = product_div.find('span', class_='amount')
            price = f"{price_tag.text.strip()}" if price_tag else "Price not found"

            # Highlight the item_name and price on the webpage using JavaScript
            if item_name_tag:
                driver.execute_script("arguments[0].style.backgroundColor = '#4682B4';", 
                                      driver.find_element(By.XPATH, f"//*[text()='{item_name}']"))
            if price_tag:
                driver.execute_script("arguments[0].style.backgroundColor = '#5F9EA0';", 
                                      driver.find_element(By.XPATH, f"//*[text()='{price_tag.text.strip()}']"))

            if (item_name, price) not in unique_products:
                unique_products.add((item_name, price))
                writer.writerow([item_name, price])

            time.sleep(0.3)  # Pause to see the highlight effect

    print(f"Data saved to {file_name}")

driver.quit()
