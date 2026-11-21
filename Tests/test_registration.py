import os
import uuid
import pytest
from dotenv import load_dotenv

from Pages.registration_page import RegistrationPage

load_dotenv()

FIRST_NAME = "Test_first_name_1"
LAST_NAME = "Test_last_name_1"

#invalid data - invalid format of email and password
INVALID_EMAIL = "test1gg.com"
PASSWORD_WITHOUT_SPECIAL_CHAR = "qwertasdfQ1"

@pytest.fixture(scope="session")
def valid_password():
    password = os.getenv("TEST_USER_PASSWORD")
    if not password:
        raise ValueError("Critical error: password not found in the environment!")
    return password

#generate unique email for each call
def get_unique_email():
    return f"test_user_reg{uuid.uuid4().hex[:8]}@gm.com"


def test_registration_form_is_available(driver):
    registration_page = RegistrationPage(driver)
    assert registration_page.is_registration_icon_displayed(), "Registration icon not found"
    registration_page.open_registration_page()
    assert registration_page.are_registration_form_elements_displayed(), "Registration form elements are not displayed"

def test_valid_registration_success(driver, valid_password):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.register(FIRST_NAME, LAST_NAME, get_unique_email(), valid_password)
    assert registration_page.get_modal_title_text() == "Registered"
    assert registration_page.get_modal_message_text() == "You are logged in success"
    registration_page.close_modal_window()
    assert registration_page.is_log_out_button_displayed(), "Log out button is not displayed after registration"

def test_invalid_registration_with_empty_first_name(driver, valid_password):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.fill_registration_form("", LAST_NAME, get_unique_email(), valid_password)
    assert registration_page.get_first_name_error_text() == "Name is required"
    assert registration_page.is_submit_button_disabled(), "Submit button must remain disabled"

def test_invalid_registration_with_empty_last_name(driver, valid_password):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.fill_registration_form(FIRST_NAME, "", get_unique_email(), valid_password)
    assert registration_page.get_last_name_error_text() == "Last name is required"
    assert registration_page.is_submit_button_disabled(), "Submit button must remain disabled"

def test_invalid_registration_with_empty_email(driver, valid_password):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.fill_registration_form(FIRST_NAME, LAST_NAME, "", valid_password)
    assert registration_page.get_email_error_text() == "Email is required"
    assert registration_page.is_submit_button_disabled(), "Submit button must remain disabled"

def test_invalid_registration_with_empty_password(driver):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.fill_registration_form(FIRST_NAME, LAST_NAME, get_unique_email(), "")
    assert registration_page.get_password_error_text() == "Password is required"
    assert registration_page.is_submit_button_disabled(), "Submit button must remain disabled"

def test_invalid_registration_with_invalid_email_format(driver, valid_password):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.fill_registration_form(FIRST_NAME, LAST_NAME, INVALID_EMAIL, valid_password)
    assert registration_page.get_email_error_text() == "Wrong email format"
    assert registration_page.is_submit_button_disabled(), "Submit button must remain disabled"

def test_invalid_registration_without_terms_checkbox(driver, valid_password):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.fill_registration_form(FIRST_NAME, LAST_NAME, get_unique_email(), valid_password, False)
    assert registration_page.is_submit_button_disabled(), "Submit button must be disabled when Terms are unchecked"

def test_invalid_registration_existing_user(driver, valid_password):
    registration_page = RegistrationPage(driver)
    existing_email = get_unique_email()

    registration_page.open_registration_page()
    registration_page.register(FIRST_NAME, LAST_NAME, existing_email, valid_password)
    assert registration_page.get_modal_title_text() == "Registered"
    registration_page.close_modal_window()
    registration_page.click_log_out_button()

    registration_page.open_registration_page()
    registration_page.register(FIRST_NAME, LAST_NAME, existing_email, valid_password)
    assert registration_page.get_modal_title_text() == "Registration failed"
    #In the error modal window, the frontend renders text inside extra quotation marks: '"User already exists"'
    assert registration_page.get_modal_message_text() == '"User already exists"'

@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Bug: Frontend allows whitespace in Name; UI renders '[object Object]' instead of field error"
)
def test_invalid_registration_with_space_in_name(driver, valid_password):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.register(" ", LAST_NAME, get_unique_email(), valid_password)

    assert registration_page.get_modal_title_text() == "Registration failed"
    assert registration_page.get_modal_message_text() == "Cannot be empty"


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Bug: Special char is mandatory despite 'Can contain' spec, and UI renders '[object Object]'"
)
def test_invalid_registration_password_without_special_char(driver):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.register(FIRST_NAME, LAST_NAME, get_unique_email(), PASSWORD_WITHOUT_SPECIAL_CHAR)

    expected_msg = (
        "At least 8 characters; Must contain at least 1 uppercase letter, "
        "1 lowercase letter, and 1 number; Can contain special characters [@$#^&*!]"
    )
    assert registration_page.get_modal_title_text() == "Registration failed"
    assert registration_page.get_modal_message_text() == expected_msg