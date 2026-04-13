import pytest
from faker import Faker

from src.web.Application import Application

fake = Faker()
invalid_login_data = [
    pytest.param("", "", id="empty_email-empty_password"),
    pytest.param("", fake.pystr(min_chars=1, max_chars=1), id="empty_email-single_char_password"),
    pytest.param(fake.email(), fake.password(length=7), id="valid_email-password_len_7"),
    pytest.param(fake.email(), fake.password(length=8), id="valid_email-password_len_8"),
    pytest.param(fake.email(), fake.password(length=9), id="valid_email-password_len_9"),
    pytest.param(fake.user_name(), fake.password(length=12), id="invalid_email_format-wrong_password"),
    pytest.param(fake.email().upper(), fake.password(length=10), id="uppercase_email-wrong_password"),
    pytest.param("admin' OR '1'='1--", fake.password(length=10), id="sql_injection_email-wrong_password"),
    pytest.param("<script>alert('xss')</script>@test.com", fake.password(length=10), id="xss_email-wrong_password"),
    pytest.param("<style>*{display:none}</style>@test.com", fake.password(length=10),
                 id="css_injection_email-wrong_password"),
]


@pytest.mark.smoke
@pytest.mark.parametrize("email, password", invalid_login_data)
def test_login_invalid(app: Application, email: str, password: str):
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(email, password)
    app.login_page.invalid_login_message_visible()


@pytest.mark.smoke
def test_login_with_valid_creds(logged_app: Application):
    logged_app.projects_page.is_loaded()
