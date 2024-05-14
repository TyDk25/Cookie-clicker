from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

COOKIE_ID = "bigCookie"
COOKIES_ID = "cookies"
PRODUCT_PRICE_PREFIX = 'productPrice'
PRODUCT_PREFIX = 'product'

# Initialize the ChromeDriver using WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://orteil.dashnet.org/cookieclicker/')


def wait_for_button_present(by_type, x_path: str):
    return WebDriverWait(driver, timeout=30).until(
        EC.element_to_be_clickable((by_type, x_path))
    )


accept_cookies = wait_for_button_present(By.XPATH, x_path='/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]')
accept_cookies.click()

select_language = wait_for_button_present(By.XPATH, '//*[@id="langSelect-EN"]')
select_language.click()

while True:
    cookie = driver.find_element(By.ID, COOKIE_ID)
    cookie.click()
    cookies_count_element = driver.find_element(By.ID, COOKIES_ID)
    cookies_count_text = cookies_count_element.text.split(" ")[0]
    cookies_count = int(cookies_count_text.replace(',', ''))

    for i in range(4):
        product_price_element = driver.find_element(By.ID, PRODUCT_PRICE_PREFIX + str(i))
        product_price_text = product_price_element.text.replace(',', '')

        # Check if the product price is a valid integer
        if not product_price_text.isdigit():
            continue

        product_price = int(product_price_text)

        if cookies_count >= product_price:
            product = driver.find_element(By.ID, PRODUCT_PREFIX + str(i))
            product.click()
            break
