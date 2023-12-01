import time

import pandas as pd
from fake_useragent import UserAgent
from selenium.webdriver import Keys
from selenium.webdriver.support.select import Select

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


# Настройка опций для Chrome
ua = UserAgent()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user_agent={ua.random}")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")


data = []

with webdriver.Chrome(options=chrome_options) as driver:
    driver.delete_all_cookies()

    driver.get("https://www.nseindia.com/")
    actions = ActionChains(driver)

    # прокрутка страницы для имитации действий пользователя
    for _ in range(10):
        driver.execute_script("window.scrollBy(0,200)")
        time.sleep(2)

    # Наведение курсора Market Data
    market_data = driver.find_element(By.CSS_SELECTOR, "a#link_2.nav-link.dd-link")
    actions.move_to_element(market_data).perform()

    # Клик на Pre Open Market
    pre_open_market = driver.find_element(
        By.CSS_SELECTOR, "ul.nav.flex-column a.nav-link"
    )
    actions.move_to_element(pre_open_market).click().perform()

    time.sleep(5)

    # Парсинг таблицы
    table = driver.find_element(By.CSS_SELECTOR, "table#livePreTable")
    rows = table.find_elements(By.CSS_SELECTOR, "tr")
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, "td")
        if len(cells) > 1:
            name = cells[1].text
            final_price = cells[6].text
            if "Total" not in name:
                data.append([name, final_price])

    # Открытие новой вкладки и переход на главную страницу
    driver.execute_script("window.open('https://www.nseindia.com/');")
    time.sleep(2)

    # Переключение на новую вкладку
    driver.switch_to.window(driver.window_handles[1])
    driver.implicitly_wait(15)

    # Выбрать график "NIFTY BANK"
    nifty_bank = driver.find_element(By.CSS_SELECTOR, "#tabList_NIFTYBANK")
    actions.move_to_element(nifty_bank).click().perform()
    time.sleep(2)

    # Нажать “View all”
    view_all = driver.find_element(
        By.CSS_SELECTOR,
        "#tab4_gainers_loosers > div.link-wrap > a[href='/market-data/live-equity-market?symbol=NIFTY BANK']",
    )
    driver.execute_script("arguments[0].click();", view_all)
    time.sleep(2)

    # На новой странице, выбрать "NIFTY ALPHA 50" в селекторе
    select_element = driver.find_element(By.CSS_SELECTOR, "#equitieStockSelect")
    select = Select(select_element)
    select.select_by_visible_text("NIFTY ALPHA 50")
    time.sleep(5)

    # Пролистать до конца таблицы
    table_element = driver.find_element(By.CSS_SELECTOR, "#equityStockTable")
    actions.move_to_element(table_element).click().perform()
    for _ in range(2):
        time.sleep(2)
        actions.send_keys(Keys.SPACE).perform()


# Выгрузка в таблицу
df = pd.DataFrame(data, columns=["Имя", "Цена"])
df.to_csv("final_prices.csv", sep=";", index=False, encoding="utf-8-sig")
print("Позиции выгружены в final_prices.csv")
