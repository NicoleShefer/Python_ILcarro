# QA54_demoIlCarro

Automated negative tests for the registration form of the iCarro demo app:
https://icarro-v1.netlify.app/register

## Baseline test data
Every test uses the valid values below, except for the one field under test.

| Field | Value |
|---|---|
| First name | `Test_first_name` |
| Last name | `Test_last_name` |
| Email | `test_user_reg<unique_uuid>@gm.com` (new one generated for each test) |
| Password | Valid password loaded from `.env` (8+ characters, with uppercase, lowercase, digit and special character) |
| Terms of use | Checkbox ticked |

## Negative scenarios

| # | Test | Input | Expected result | Status |
|---|---|---|---|---|
| 1 | `test_invalid_registration_with_empty_name` | First name is empty | "Name is required" appears under the field; the "Y'alla!" button is disabled | Passed |
| 2 | `test_invalid_registration_with_empty_last_name` | Last name is empty | "Last name is required" appears under the field; the button is disabled | Passed |
| 3 | `test_invalid_registration_with_empty_email` | Email is empty | "Email is required" appears under the field; the button is disabled | Passed |
| 4 | `test_invalid_registration_with_invalid_email_format` | Email without "@" (`test1gg.com`) | After the field loses focus, "Wrong email format" appears; the button is disabled | Passed |
| 5 | `test_invalid_registration_with_empty_password` | Password is empty | "Password is required" appears under the field; the button is disabled | Passed |
| 6 | `test_invalid_registration_without_terms_checkbox` | Terms checkbox is unticked | The button stays disabled | Passed |
| 7 | `test_invalid_registration_existing_user` | Email that is already registered | The button is enabled; after submitting, the server returns 400 Bad Request and a modal shows "User already exists" | Passed |
| 8 | `test_invalid_registration_with_space_in_name` | First name is a single space | A validation error or a readable server message | Bug (`xfail`) |
| 9 | `test_invalid_registration_password_without_special_char` | `asdfghjklasdfaQ1` (no special character) | A password format hint with the button blocked, or a modal listing the password requirements | Bug (`xfail`) |

## Known defects

### Scenario 8: space-only first name
- Client-side validation treats a space as a valid value and enables the "Y'alla!" button.
- The server responds with 400 Bad Request and a JSON object like `{"firstName": "must not be empty"}`. The message is localized in Russian even though the UI is in English.
- The frontend cannot parse the object, so the modal shows `[object Object]`.

### Scenario 9: password without a special character
Expected modal text: *"At least 8 characters; Must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number; Can contain special characters [@$#^&*!]"*

- The frontend does no password complexity check, so the "Y'alla!" button becomes active.
- The backend wording says special characters are optional ("can contain"), yet the server rejects the password with 400 Bad Request.
- The modal shows `[object Object]` instead of a readable error.

Both tests are marked with `@pytest.mark.xfail` in the code.
