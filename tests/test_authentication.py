from playwright.sync_api import expect
import os
from redis import StrictRedis
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
redis = StrictRedis(host='localhost', port=6379, db=0, password=REDIS_PASSWORD)
os.environ['REDIS_TIMEOUT'] = '3'


def test_sign_up_page_sign_up_successful(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Sign up'")
    page.fill(".sign-up-name-card", "Peter Parker")
    page.fill(".sign-up-user_name-card", "parker89")
    page.fill(".sign_up-password-card", "Matter343*")
    page.fill(".sign_up-c-password-card", "Matter343*")
    page.select_option("select[name=birth_day]", value='22')
    page.select_option("select[name=birth_month]", value='May')
    page.select_option("select[name=birth_year]", value='1999')
    page.click("text='Confirm & sign up'")
    success = page.locator(".log_in_success")
    expect(success).to_have_text("Welcome to your Chitter, parker89!")


def test_sign_up_page_sign_up_no_input(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Sign up'")
    page.click("text='Confirm & sign up'")
    errors = page.locator(".sign_up_error")
    expect(errors).to_have_text(['Please provide a name!',
        'Please choose a username!',
        'Password must be at least 8 characters.',
        'Password must contain uppercase and lowercase characters.',
        'Password must contain at least 1 number.',
        'Password must contain at least 1 symbol.'
    ])


def test_sign_up_page_sign_up_used_user_name(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Sign up'")
    page.fill(".sign-up-name-card", "Peter Parker")
    page.fill(".sign-up-user_name-card", "son_of_john")
    page.fill(".sign_up-password-card", "Matter343*")
    page.fill(".sign_up-c-password-card", "Matter343*")
    page.select_option("select[name=birth_day]", value='22')
    page.select_option("select[name=birth_month]", value='May')
    page.select_option("select[name=birth_year]", value='1999')
    page.click("text='Confirm & sign up'")
    error = page.locator(".sign_up_error")
    expect(error).to_have_text("Username taken!")


def test_sign_up_page_sign_up_non_matching_passwords(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Sign up'")
    page.fill(".sign-up-name-card", "Peter Parker")
    page.fill(".sign-up-user_name-card", "parker11")
    page.fill(".sign_up-password-card", "Matter343*")
    page.fill(".sign_up-c-password-card", "Matte343*")
    page.select_option("select[name=birth_day]", value='22')
    page.select_option("select[name=birth_month]", value='May')
    page.select_option("select[name=birth_year]", value='1999')
    page.click("text='Confirm & sign up'")
    error = page.locator(".sign_up_error")
    expect(error).to_have_text("Passwords do not match!")


def test_log_in_login_in_successful(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    success = page.locator(".log_in_success")
    expect(success).to_have_text("Welcome to your Chitter, son_of_john!")


def test_log_in_login_in_no_input(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Log in'")
    error = page.locator(".log_in_error")
    expect(error).to_have_text("Enter your username and password.")


def test_log_in_login_in_no_password(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.click("text='Log in'")
    error = page.locator(".log_in_error")
    expect(error).to_have_text("Enter your password.")


def test_log_in_login_in_no_user_name(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    error = page.locator(".log_in_error")
    expect(error).to_have_text("Enter your username.")


def test_log_in_login_in_incorrect_password(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never001")
    page.click("text='Log in'")
    error = page.locator(".log_in_error")
    expect(error).to_have_text("Something doesn't match there!")


def test_log_in_login_in_user_name_does_not_exist(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_kate")
    page.fill(".password-tag", "Never00*")
    page.click("text='Log in'")
    error = page.locator(".log_in_error")
    expect(error).to_have_text("Something doesn't match there!")


def test_log_in_too_many_attempts(page, test_web_address, db_connection):
    redis.flushall()
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    for _ in range(4):
        page.fill(".user-name-tag", "son_of_john")
        page.fill(".password-tag", "Never00*")
        page.click("text='Log in'")
        error = page.locator(".log_in_error")
        expect(error).to_have_text("Something doesn't match there!")
    for _ in range(3):
        page.fill(".user-name-tag", "son_of_john")
        page.fill(".password-tag", "Never00*")
        page.click("text='Log in'")
        error = page.locator(".log_in_error")
        expect(error).to_have_text("Too many tries! Wait 2 minutes.")
    page.wait_for_timeout(3000)
    for _ in range(4):
        page.fill(".user-name-tag", "son_of_john")
        page.fill(".password-tag", "Never00*")
        page.click("text='Log in'")
        error = page.locator(".log_in_error")
        expect(error).to_have_text("Something doesn't match there!")
    for _ in range(3):
        page.fill(".user-name-tag", "son_of_john")
        page.fill(".password-tag", "Never00*")
        page.click("text='Log in'")
        error = page.locator(".log_in_error")
        expect(error).to_have_text("Too many tries! Wait 2 minutes.")
