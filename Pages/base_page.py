from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:

    #common locators (header) for each page
    REGISTRATION_ICON = (By.CSS_SELECTOR, "[href='/register']")
    LOG_OUT_BUTTON = (By.XPATH, "//button[text()='Log out']")

    def __init__(self, driver):
        self.driver = driver

    def is_element_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_until_invisible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def is_element_disabled(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return not element.is_enabled()
        except TimeoutException as e:
            raise TimeoutException(f"Element {locator} was not found in DOM within {timeout} sec. Unable to validate the disabled attribute.") from e

    def click_element(self, locator, timeout=10):
        # For a click, it's more reliable to wait for clickability, not just visibility.
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def input_text(self, locator, text, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element.click()
        element.clear()
        if text:
            element.send_keys(text)
        #move focus to get blur/touched validator
        element.send_keys(Keys.TAB)

    def get_element_text(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d:d.find_element(*locator).is_displayed()
            and d.find_element(*locator).text.strip() != ""
        )
        return self.driver.find_element(*locator).text

    def get_alert_text(self, text, timeout=10):
        alert = WebDriverWait(self.driver, timeout).until(
           EC.alert_is_present()
        )
        return alert.text

    def accept_alert(self, timeout=10):
        alert = WebDriverWait(self.driver, timeout).until(
            EC.alert_is_present()
        )
        alert.accept()

    #header navigation (common)

    def is_registration_icon_displayed(self):
        return self.is_element_visible(self.REGISTRATION_ICON)

    def open_registration_page(self):
        self.click_element(self.REGISTRATION_ICON)

    def is_log_out_button_displayed(self):
        return self.is_element_visible(self.LOG_OUT_BUTTON)

    def click_log_out_button(self):
        self.click_element(self.LOG_OUT_BUTTON)