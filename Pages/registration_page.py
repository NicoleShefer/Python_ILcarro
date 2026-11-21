from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class RegistrationPage(BasePage):

    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    EMAIL_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    TERM_OF_USE_CHECK_BOX = (By.ID, "terms-of-use")
    REGISTRATION_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    #Server response Modal window locators (linked via h3 + p adjacency, no blind tag search)
    MODAL_OVERLAY = (By.CSS_SELECTOR, ".modal-overlay")
    MODAL_TITLE = (By.CSS_SELECTOR, ".modal-content h3")
    MODAL_MESSAGE = (By.CSS_SELECTOR, ".modal-content p")
    OK_BUTTON = (By.CSS_SELECTOR, ".modal-content button")

    #Error messages
    FIRST_NAME_ERROR = (By.CSS_SELECTOR, "input[name='firstName'] ~ div.error")
    LAST_NAME_ERROR = (By.CSS_SELECTOR, "input[name='lastName'] ~ div.error")
    EMAIL_ERROR = (By.CSS_SELECTOR, "input[name='username'] ~ div.error")
    PASSWORD_ERROR = (By.CSS_SELECTOR, "input[name='password'] ~ div.error")

    def are_registration_form_elements_displayed(self):
        return (self.is_element_visible(self.FIRST_NAME_INPUT)
                and self.is_element_visible(self.LAST_NAME_INPUT)
                and self.is_element_visible(self.EMAIL_INPUT)
                and self.is_element_visible(self.PASSWORD_INPUT)
                and self.is_element_visible(self.TERM_OF_USE_CHECK_BOX)
                and self.is_element_visible(self.REGISTRATION_BUTTON))


    def fill_first_name_field(self, first_name):
        self.input_text(self.FIRST_NAME_INPUT, first_name)

    def fill_last_name_field(self, last_name):
        self.input_text(self.LAST_NAME_INPUT, last_name)

    def fill_email_field(self, email):
        self.input_text(self.EMAIL_INPUT, email)

    def fill_password_field(self, password):
        self.input_text(self.PASSWORD_INPUT, password)

    def click_term_of_use_checkbox(self):
        self.click_element(self.TERM_OF_USE_CHECK_BOX)

    def click_registration_button(self):
        self.click_element(self.REGISTRATION_BUTTON)

    def is_submit_button_disabled(self):
        return self.is_element_disabled(self.REGISTRATION_BUTTON)

    def get_first_name_error_text(self):
        return self.get_element_text(self.FIRST_NAME_ERROR)

    def get_last_name_error_text(self):
        return self.get_element_text(self.LAST_NAME_ERROR)

    def get_email_error_text(self):
        return self.get_element_text(self.EMAIL_ERROR)

    def get_password_error_text(self):
        return self.get_element_text(self.PASSWORD_ERROR)

    def get_modal_title_text(self):
        return self.get_element_text(self.MODAL_TITLE)

    def get_modal_message_text(self):
        return self.get_element_text(self.MODAL_MESSAGE)

    def close_modal_window(self):
        self.click_element(self.OK_BUTTON)
        self.wait_until_invisible(self.MODAL_OVERLAY)

    def fill_registration_form(self, first_name, last_name, email, password, agree_terms=True):
        self.fill_first_name_field(first_name)
        self.fill_last_name_field(last_name)
        self.fill_email_field(email)
        self.fill_password_field(password)
        if agree_terms:
            self.click_term_of_use_checkbox()

    def register(self, first_name, last_name, email, password):
        self.fill_registration_form(first_name, last_name, email, password, agree_terms=True)
        self.click_registration_button()