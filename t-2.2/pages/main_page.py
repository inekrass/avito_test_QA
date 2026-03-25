import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    MIN_PRICE_INPUT = (By.XPATH, "//input[@type='number' and @placeholder='От']")
    MAX_PRICE_INPUT = (By.XPATH, "//input[@type='number' and @placeholder='До']")
    PAGE_READY_TEXT = (By.XPATH, "//*[contains(text(), 'Модерация объявлений')]")

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.PAGE_READY_TEXT))

    def set_price_range(self, min_price, max_price):
        min_input = self.wait.until(EC.visibility_of_element_located(self.MIN_PRICE_INPUT))
        max_input = self.wait.until(EC.visibility_of_element_located(self.MAX_PRICE_INPUT))

        min_input.clear()
        min_input.send_keys(str(min_price))

        max_input.clear()
        max_input.send_keys(str(max_price))

    def extract_visible_prices(self):
        text = self.driver.find_element(By.TAG_NAME, "body").text
        raw_prices = re.findall(r"(\d[\d\s]*)\s*₽", text)
        return [int(price.replace(" ", "")) for price in raw_prices]

    def has_empty_state(self):
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        return "Объявления не найдены" in body_text
