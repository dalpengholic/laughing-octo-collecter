from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import sqlite3
from datetime import datetime
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os

remote_driver_ip = os.environ['REMOTE_DRIVER_IP']
print(remote_driver_ip)
import selenium
selenium.__version__

## Remote webdriver
def test_selenium_server_available():
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry

    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)

    session.get(f"http://{remote_driver_ip}:4444/wd/hub")

def get_shadow_root(driver):
    shadow_host = driver.find_element(By.CSS_SELECTOR, '#usercentrics-root')
    return shadow_host.shadow_root

def click_shadow_button(shadow_root):
    shadow_container = shadow_root.find_element(By.CSS_SELECTOR, '#uc-center-container')
    shadow_btns = shadow_container.find_elements(By.TAG_NAME, 'button')
    shadow_btns[2].click()

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, 1000);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def get_product_data(driver):
    product_names = driver.find_elements(By.XPATH, '//a[@data-test-id="product-card__productName"]')
    product_prices = driver.find_elements(By.XPATH, '//div[@data-test-id="product-card__productPrice__comparisonPrice"]')
    return list(zip(product_names, product_prices))

def save_to_database(data):
    conn = sqlite3.connect("./data/suomi_milk_product_data.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, product_name TEXT, product_price TEXT, date TEXT)")
    today = datetime.now().strftime("%Y-%m-%d")
    for index, (product_name, product_price) in enumerate(data):
        try:
            c.execute("INSERT INTO products (id, product_name, product_price, date) VALUES (?, ?, ?, ?)", (index, product_name.text, product_price.text, today))
        except sqlite3.IntegrityError as e:
            c.execute("UPDATE products SET product_name=?, product_price=?, date=? WHERE id=?", (product_name.text, product_price.text, today, index))
    conn.commit()
    conn.close()

def collect_data():
    test_selenium_server_available()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Remote(f'http://{remote_driver_ip}:4444/wd/hub', options=chrome_options)
    url = 'https://www.s-kaupat.fi/tuotteet/maito-munat-ja-rasvat-0/maidot-ja-piimat/maidot?queryString=maito'
    driver.get(url)
    #time.sleep(3)
    scroll_to_bottom(driver)
    time.sleep(3)
    shadow_root = get_shadow_root(driver)
    click_shadow_button(shadow_root)
    scroll_to_bottom(driver)
    time.sleep(3)
    product_data = get_product_data(driver)
    for index, (product_name, product_price) in enumerate(product_data):
        print(index, product_name.text)
        print(product_price.text)
    save_to_database(product_data)
    driver.close()

if __name__ == '__main__':
    collect_data()
