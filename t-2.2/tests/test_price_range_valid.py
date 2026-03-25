import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.main_page import MainPage


def test_valid_price_range(driver, base_url):
    min_price = 1000
    max_price = 50000

    page = MainPage(driver)
    page.open(base_url)
    page.set_price_range(min_price=min_price, max_price=max_price)

    all_prices = []
    max_pages = 30
    visited_pages = 0

    while True:
        visited_pages += 1
        if visited_pages > max_pages:
            break

        prices = []
        for _ in range(10):
            prices = page.extract_visible_prices()
            if prices or page.has_empty_state():
                break
            time.sleep(0.5)

        all_prices.extend(prices)

        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Следующая страница']"))
            )

            if (
                next_button.get_attribute("disabled")
                or next_button.get_attribute("aria-disabled") == "true"
            ):
                break

            old_body_text = driver.find_element(By.TAG_NAME, "body").text

            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Следующая страница']"))
            ).click()

            WebDriverWait(driver, 5).until(
                lambda d: d.find_element(By.TAG_NAME, "body").text != old_body_text
            )

        except TimeoutException:
            break

    assert all_prices, (
        "BUG: После применения валидного диапазона цен (1000-50000) "
        "на страницах не найдено ни одной цены в объявлениях."
    )

    out_of_range = [price for price in all_prices if price < min_price or price > max_price]

    assert not out_of_range, (
        "BUG: Найдены объявления с ценами вне диапазона 1000-50000. "
        f"Проблемные цены: {out_of_range}"
    )