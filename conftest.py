import pytest
from selenium import webdriver

EMAIL = "nikastar@gmail.com"
PASSWORD = "Asdasdasd20!"


@pytest.fixture
def driver():
    driver = webdriver.Chrome()

    driver.maximize_window()
    driver.get("https://icarro-v1.netlify.app/search?page=0&size=10")
    yield driver
    driver.quit()