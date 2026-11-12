import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Фикстура: запускает браузер перед тестом и закрывает его после
@pytest.fixture
def browser():
    # Инициализация драйвера Chrome
    driver = webdriver.Chrome()
    # Разворачиваем окно на весь экран
    driver.maximize_window()
    # Передаем драйвер в тест
    yield driver
    # Закрываем браузер после завершения теста
    driver.quit()


# ТЕСТ 1: Позитивный (Проверка, что поиск находит товар)
def test_search_positive(browser):
    browser.get("https://s-tallia.ru/")

    # Ждем до 10 секунд, пока появится поле поиска
    wait = WebDriverWait(browser, 10)
    # ВАЖНО: Замените 'input[name="search"]' на реальный селектор с сайта (через F12)
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="q"]')))

    # Вводим запрос и нажимаем Enter
    search_input.send_keys("бюстгальтер")
    search_input.send_keys(Keys.ENTER)

    # Ждем 2 секунды, пока загрузятся результаты (временное решение)
    time.sleep(2)


    # Проверяем, что на странице нет текста "Ничего не найдено"
    page_source = browser.page_source
    assert "Ничего не найдено" not in page_source, "БАГ: Поиск не нашел существующий товар!"


# ТЕСТ 2: Негативный (Проверка мусорного запроса)
def test_search_negative(browser):
    browser.get("https://s-tallia.ru/")

    wait = WebDriverWait(browser, 10)
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="q"]')))

    search_input.send_keys("абракадаброкс")
    search_input.send_keys(Keys.ENTER)

    # Ждем 2 секунды, пока загрузятся результаты (временное решение)
    time.sleep(2)


    # Проверяем, что система корректно сообщила об отсутствии результатов
    page_source = browser.page_source
    assert "Ничего не найдено" in page_source or "Сожалеем" in page_source, "БАГ: Нет сообщения об отсутствии результатов!"