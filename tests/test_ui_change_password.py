from playwright.sync_api import expect
import os
os.environ['REDIS_TIMEOUT'] = '1'


def test_change_password(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    page.click("text='Change Password'")
    page.fill("#old_password", "Never00!")
    page.fill("#new_password", "Revenge13^")
    page.fill("#c_new_password", "Revenge13^")
    page.click("text='Lock Securely'")
    success_box = page.locator(".success-box")
    expect(success_box).to_have_text(['Your password was successfully changed.\nBack to profile'])
    page.click("text='Back to profile'")
    page.click("text='Log out'")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    error = page.locator(".log_in_error")
    expect(error).to_have_text("Something doesn't match there!")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Revenge13^")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    profile_info = page.locator('.profile-info-box')
    moods = "\ncontent\nexcited\nfabulous\nangry\nlet down\nlucky\nanxious\nworried\nscared\nsad\ncalm\nbuzzing\nhappy\nokay\nbored"
    expect(profile_info).to_have_text('Real name:\nJohnson\nCake day:\n'
                                    '19 October\nCurrent mood:' + moods + '\nLikes to peep at peeps about:\n'
                                    '#DaysOut\n#Food\n#Festivals\nSelect preferred tags\n'
                                    'Account Security:\nChange Password\nDelete Profile')


def test_change_password_invalid(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    page.wait_for_timeout(3000)
    page.click("text='Change Password'")
    page.fill("#old_password", "Never0!")
    page.fill("#new_password", "akfjs")
    page.fill("#c_new_password", "akfjs")
    page.click("text='Lock Securely'")
    error = page.locator(".cp_error")
    expect(error).to_have_text("Current password did not match!")
    page.fill("#old_password", "Never00!")
    page.fill("#new_password", "akfjs")
    page.fill("#c_new_password", "akfjs")
    page.click("text='Lock Securely'")
    errors = page.locator(".cp_error")
    expect(errors).to_have_text([
        'Password must be at least 8 characters.',
        'Password must contain uppercase and lowercase characters.',
        'Password must contain at least 1 number.',
        'Password must contain at least 1 symbol.'
    ])


def test_change_password_current_password_blank(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    page.click("text='Change Password'")
    page.fill("#old_password", "")
    page.fill("#new_password", "Wonderland8*")
    page.fill("#c_new_password", "Wonderland8*")
    page.click("text='Lock Securely'")
    error = page.locator(".cp_error")
    expect(error).to_have_text("Enter your current password.")
    page.fill("#old_password", " ")
    page.fill("#new_password", "Wonderland8*")
    page.fill("#c_new_password", "Wonderland8*")
    page.click("text='Lock Securely'")
    error = page.locator(".cp_error")
    expect(error).to_have_text("Enter your current password.")


def test_change_password_new_password_blank(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    page.click("text='Change Password'")
    page.fill("#old_password", "Never00!")
    page.fill("#new_password", "Wonderland8*")
    page.fill("#c_new_password", "")
    page.click("text='Lock Securely'")
    error = page.locator(".cp_error")
    expect(error).to_have_text("Enter your new password twice to confirm.")
    page.fill("#old_password", "Never00!")
    page.fill("#new_password", "")
    page.fill("#c_new_password", "Wonderland8*")
    page.click("text='Lock Securely'")
    error = page.locator(".cp_error")
    expect(error).to_have_text("Enter your new password twice to confirm.")
    page.fill("#old_password", "Never00!")
    page.fill("#new_password", "Wonderland8*")
    page.fill("#c_new_password", " ")
    page.click("text='Lock Securely'")
    error = page.locator(".cp_error")
    expect(error).to_have_text("Enter your new password twice to confirm.")
    page.fill("#old_password", "Never00!")
    page.fill("#new_password", " ")
    page.fill("#c_new_password", "Wonderland8*")
    page.click("text='Lock Securely'")
    error = page.locator(".cp_error")
    expect(error).to_have_text("Enter your new password twice to confirm.")
