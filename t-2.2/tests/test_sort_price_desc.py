import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.main_page import MainPage


def test_sort_by_price_desc(driver, base_url):
    page = MainPage(driver)
    page.open(base_url)
    page.set_sorting(sort_by="Цене", sort_order="По убыванию")

    deadline = time.time() + 120
    timed_out = False
    page_number = 1
    checked_pages = 0
    previous_page_last_price = None
    page_violations = []
    boundary_violations = []

    while True:
        if time.time() > deadline:
            timed_out = True
            break

        prices = []
        for _ in range(10):
            prices = page.extract_visible_prices()
            if prices or page.has_empty_state():
                break
            time.sleep(0.5)

        assert prices, (
            "BUG: После применения сортировки по цене по убыванию "
            f"на странице {page_number} не найдено ни одной цены."
        )

        checked_pages += 1

        if previous_page_last_price is not None and prices[0] > previous_page_last_price:
            boundary_violations.append(
                (page_number - 1, previous_page_last_price, page_number, prices[0])
            )

        violations = [
            (index, left, right)
            for index, (left, right) in enumerate(zip(prices, prices[1:]), start=1)
            if left < right
        ]
        if violations:
            page_violations.append((page_number, violations[0]))

        previous_page_last_price = prices[-1]

        next_buttons = driver.find_elements(By.XPATH, "//button[@aria-label='Следующая страница']")
        if not next_buttons:
            break

        next_button = next_buttons[0]
        if (
            next_button.get_attribute("disabled")
            or next_button.get_attribute("aria-disabled") == "true"
        ):
            break

        old_body_text = driver.find_element(By.TAG_NAME, "body").text

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Следующая страница']"))
        ).click()

        try:
            WebDriverWait(driver, 5).until(
                lambda d: d.find_element(By.TAG_NAME, "body").text != old_body_text
            )
        except TimeoutException as exc:
            raise AssertionError(
                f"BUG: После клика на следующую страницу контент не обновился на странице {page_number}."
            ) from exc

        page_number += 1

    assert checked_pages > 0, "BUG: Не удалось проверить ни одной страницы выдачи."

    assert not timed_out, (
        "BUG: Тест превысил лимит 120 секунд при обходе страниц. "
        "Возможна зацикленная пагинация или нестабильная загрузка данных."
    )

    assert not page_violations, (
        "BUG: На одной из страниц список объявлений не отсортирован по цене по убыванию. "
        f"Первая ошибка на странице {page_violations[0][0]}: "
        f"позиция {page_violations[0][1][0]}, "
        f"{page_violations[0][1][1]} < {page_violations[0][1][2]}"
    )

    assert not boundary_violations, (
        "BUG: Нарушен порядок цен между страницами при сортировке по убыванию. "
        f"Граница страниц {boundary_violations[0][0]}->{boundary_violations[0][2]}: "
        f"последняя цена предыдущей страницы {boundary_violations[0][1]}, "
        f"первая цена следующей страницы {boundary_violations[0][3]}"
    )
