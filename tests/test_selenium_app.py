import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_home_page(browser):
    browser.get("http://127.0.0.1:5000/")
    assert "MovieWeb" in browser.page_source

def test_add_user_ui(browser):
    browser.get("http://127.0.0.1:5000/add_user")
    name_field = browser.find_element(By.NAME, "name")
    name_field.send_keys("UIUser")
    submit_btn = browser.find_element(By.XPATH, "//button[@type='submit']")
    submit_btn.click()
    time.sleep(1)
    assert "UIUser" in browser.page_source
