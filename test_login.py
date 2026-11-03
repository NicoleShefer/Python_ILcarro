import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import EMAIL, PASSWORD

URL = "https://icarro-v1.netlify.app/login"
SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
ERROR = (By.XPATH, "//*[contains(text(), 'Login or Password incorrect')]")


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get(URL)
    yield driver
    driver.quit()


def fill_form(driver, email, password):
    """Wait for the form to load, then fill in the email and password fields."""
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)


class TestLogin:
    def test_successful_login(self, driver):
        """Valid email and password: the user is logged in and the URL changes."""
        fill_form(driver, EMAIL, PASSWORD)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable(SUBMIT)).click()

        assert wait.until(EC.url_changes(URL)), "Login failed: the URL did not change"

    def test_login_wrong_password(self, driver):
        """Registered email and wrong password: the 'Login failed' error is shown."""
        fill_form(driver, EMAIL, "WrongPass123!")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable(SUBMIT)).click()

        error = wait.until(EC.visibility_of_element_located(ERROR))
        assert error.is_displayed(), "The 'Login failed' message was not displayed"
        assert "/login" in driver.current_url, "User must stay on the login page"

    def test_login_empty_password(self, driver):
        """Valid email and empty password: the submit button stays disabled."""
        fill_form(driver, EMAIL, "")

        assert not driver.find_element(*SUBMIT).is_enabled(), \
            "Submit button must be disabled when the password is empty"
        assert "/login" in driver.current_url, "User must stay on the login page"

    def test_login_invalid_email(self, driver):
        """Invalid email format and valid password: the submit button stays disabled."""
        fill_form(driver, "nika.gmail.com", PASSWORD)

        assert not driver.find_element(*SUBMIT).is_enabled(), \
            "Submit button must be disabled when the email format is invalid"
        assert "/login" in driver.current_url, "User must stay on the login page"