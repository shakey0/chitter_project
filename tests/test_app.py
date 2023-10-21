from playwright.sync_api import expect
from datetime import datetime
from freezegun import freeze_time

months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
        7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

select_tags_box = "×\nSelect Tags for Peep\n#DaysOut\n#Food\n#Travel\n#Hobbies\n#Festivals\n#Music"\
                "\n#Art\n#Nature\n#Social\n#Work\n#Creative\n#Books\nConfirm"
delete_box = "Are you sure you want to delete this peep?\nConfirm\nCancel"

@freeze_time("2023-09-07 12:00:01")
def test_time():
    assert datetime.now() == datetime(2023, 9, 7, 12, 0, 1)

def test_top_bar_homepage_unauthenticated(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    user_name_tag = page.locator(".user-name-tag")
    placeholder_value = user_name_tag.get_attribute("placeholder")
    assert placeholder_value == 'Username'
    password_tag = page.locator(".password-tag")
    placeholder_value = password_tag.get_attribute("placeholder")
    assert placeholder_value == 'Password'
    log_in_button = page.locator(".log-in-button")
    expect(log_in_button).to_have_text('Log in')
    not_member_tag = page.locator(".not-member-tag")
    expect(not_member_tag).to_have_text('Not a member?')
    sign_up_button = page.locator(".sign-up-button")
    expect(sign_up_button).to_have_text('Sign up')

def test_peeps_homepage_unauthenticated(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        'sammy1890\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def test_homepage_unauthenticated_click_user_name(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='jodesnode'")
    authentication = page.locator(".log_in_error")
    expect(authentication).to_have_text("Log in or sign up to view user profiles!")

def test_homepage_unauthenticated_click_peep_at_images(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Peep at the pictures'")
    pop_up_box = page.locator('.picture-peep-box')
    expect(pop_up_box).to_have_text('mousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.')

def test_homepage_unauthenticated_click_user_name_on_image(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Peep at the pictures'")
    page.click('.picture-peep-box >> a:has-text("mousey_14")')
    authentication = page.locator(".log_in_error")
    expect(authentication).to_have_text("Log in or sign up to view user profiles!")

def test_homepage_unauthenticated_click_sign_up(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Sign up'")
    header = page.locator('h1')
    expect(header).to_have_text('Sign Up to Chitter')
    name_card = page.locator(".sign-up-name-card")
    placeholder_value = name_card.get_attribute("placeholder")
    assert placeholder_value == 'Name'
    user_name_card = page.locator(".sign-up-user_name-card")
    placeholder_value = user_name_card.get_attribute("placeholder")
    assert placeholder_value == 'Username'
    password_message = page.locator('.sign-up-password-message')
    expect(password_message).to_have_text('Password must include at least one:\nUppercase character\nLowercase character\nNumber\nSymbol')
    password_card = page.locator(".sign_up-password-card")
    placeholder_value = password_card.get_attribute("placeholder")
    assert placeholder_value == 'Password'
    c_password_card = page.locator(".sign_up-c-password-card")
    placeholder_value = c_password_card.get_attribute("placeholder")
    assert placeholder_value == 'Confirm password'
    d_o_b_part = page.locator('.sign-up-d_o_b-tag')
    days = ''
    for num in range(1, 32):
        days += f'\n{num}'
    months = '\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember'
    current_year = datetime.now().year
    years = ''
    for num in range(1900, current_year-9):
        years += f'\n{num}'
    expect(d_o_b_part).to_have_text('Select your date of birth:' + days + months + years)
    confirm_sign_up = page.locator('.sign-up-confirm-card')
    expect(confirm_sign_up).to_have_text('Confirm & sign up')

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

def test_top_bar_homepage_authenticated(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    all_lines = page.locator(".top-bar-box")
    tags = "\nAll tags\n#DaysOut\n#Food\n#Travel\n#Hobbies\n#Festivals\n#Music\n#Art\n#Nature\n#Social\n#Work\n#Creative\n#Books"
    moods = "\ncontent\nexcited\nfabulous\nangry\nlet down\nlucky\nanxious\nworried\nscared\nsad\ncalm\nbuzzing\nhappy\nokay\nbored"
    expect(all_lines).to_have_text('Viewing:' + tags + '\nMood:' + moods + '\nson_of_john\nView Profile\nLog out')

def test_peeps_homepage_authenticated(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def test_homepage_view_tags(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.select_option("select[name=by_tag]", value='11')
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])
    page.select_option("select[name=by_tag]", value='9')
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        'rosy_red\n15 January at 16:35\nParty at mine tonight!\nThere are no pictures...\nLike\nLiked by 3 peepers\n#Music\n#Social',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n11 August at 15:22\nWho wants to go for food tonight?\nThere are no pictures...\nLiked\nLiked by 5 peepers\n#Food\n#Social'
    ])

def test_homepage_view_tags_persists_in_session(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.select_option("select[name=by_tag]", value='11')
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])
    page.click("text='Like'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLiked\nLiked by 45331 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])
    page.click("text='Post a peep'")
    page.fill(".comment-box", "This is a new peep.")
    keys_to_check = [5, 11]
    for key in keys_to_check:
        checkbox_selector = f'#tag{key}'
        page.check(checkbox_selector)
    page.click("text='Post that peep!'")
    month, day, hour, minute = add_zero(datetime.now().month), add_zero(datetime.now().day), add_zero(datetime.now().hour), add_zero(datetime.now().minute)
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n{day} {months[int(month)]} at {hour}:{minute}\nThis is a new peep.\nThere are no pictures...\nLike\nReady for peeping\n#Festivals\n#Creative',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLiked\nLiked by 45331 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def test_homepage_view_tags_resets_when_loading_user_page(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.select_option("select[name=by_tag]", value='11')
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])
    page.click("text='mousey_14'")
    page.click('a.home-button-single svg')
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def test_homepage_view_tags_resets_when_logging_out(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.select_option("select[name=by_tag]", value='11')
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])
    page.click("text='Log out'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        'sammy1890\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def test_homepage_change_mood(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.select_option("select[name=mood]", value='7')
    page.click("text='Log out'")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='sammy1890'")
    mood = page.locator(".profile-mood-tag")
    expect(mood).to_have_text('Current mood:\nanxious')
    page.goto(f"http://{test_web_address}")
    page.select_option("select[name=mood]", value='13')
    page.click("text='Log out'")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='son_of_john'")
    mood = page.locator(".profile-mood-tag")
    expect(mood).to_have_text('Current mood:\nhappy')
    

def add_zero(number):
    if len(str(number)) == 1:
        return f"0{number}"
    return str(number)

def test_homepage_add_peep_successful(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='Post a peep'")
    page.fill(".comment-box", "This is a new peep.")
    keys_to_check = [1, 3]
    for key in keys_to_check:
        checkbox_selector = f'#tag{key}'
        page.check(checkbox_selector)
    page.click("text='Post that peep!'")
    month, day, hour, minute = add_zero(datetime.now().month), add_zero(datetime.now().day), add_zero(datetime.now().hour), add_zero(datetime.now().minute)
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n{day} {months[int(month)]} at {hour}:{minute}\nThis is a new peep.\nThere are no pictures...\nLike\nReady for peeping\n#DaysOut\n#Travel',
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def test_homepage_add_peep_error(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='Post a peep'")
    page.click("text='Post that peep!'")
    error = page.locator(".peep_error")
    expect(error).to_have_text("Peeps need literate or visual content!")

def test_homepage_authenticated_click_user_name(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='jodesnode'")
    header = page.locator('.v-user-header-tag')
    expect(header).to_have_text("jodesnode's Profile")
    profile_info = page.locator('.profile-info-box')
    expect(profile_info).to_have_text('Real name:\nJody\nCake day:\n'
                                    '06 August\nCurrent mood:\ncalm\nLikes to peep at peeps about:\n'
                                    '#DaysOut\n#Travel\n#Festivals')
    header = page.locator('h2')
    expect(header).to_have_text("jodesnode's Peeps")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'jodesnode\n01 January at 00:04\nHappy New Year from South Korea!\nThere are no pictures...\nLiked\nLiked by 130 peepers\n#Travel\n#Festivals',
        'jodesnode\n23 August at 10:02\nPhotos from my holiday in spain.\nThere are no pictures...\nLike\nLiked by 10 peepers\n#Travel\n#Nature',
        'jodesnode\n10 August at 19:10\nI went to Summerfield park today.\nThere are no pictures...\nLike\nLiked by 4 peepers\n#DaysOut\n#Nature'
    ])

def test_homepage_authenticated_click_like(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='Like'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLiked\nLiked by 45331 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def test_homepage_authenticated_click_liked(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='Liked'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLike\nLiked by 55 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def test_homepage_authenticated_click_peep_at_images_plus_buttons(
        page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='Peep at the pictures'")
    pop_up_box = page.locator('#picture-peep-box-14')
    expect(pop_up_box).to_have_text('mousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.')
    page.click('#picture-peep-box-14 >> a:has-text("mousey_14")')
    header = page.locator('.v-user-header-tag')
    expect(header).to_have_text("mousey_14's Profile")
    profile_info = page.locator('.profile-info-box')
    expect(profile_info).to_have_text('Real name:\nAlice\n Cake day:\n'
                                    '31 May\nCurrent mood:\ncontent\nLikes to peep at peeps about:\n'
                                    '#DaysOut\n#Travel\n#Hobbies')
    header = page.locator('h2')
    expect(header).to_have_text("mousey_14's Peeps")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        'mousey_14\n31 August at 18:52\nDelicious 4 cheese pizza I made!\nThere are no pictures...\nLike\nLiked by 24 peepers\n#Food\n#Hobbies\n#Art'
    ])

def test_homepage_click_amend_tags(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='Amend tags'")
    keys_to_check = [2, 7]
    for key in keys_to_check:
        checkbox_selector = f'#amend-p-t-box-13 #tag{key}'
        page.check(checkbox_selector)
    page.uncheck('#amend-p-t-box-13 #tag4')
    page.click("text='Confirm'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'sammy1890\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 February at 19:45\nMy fantastic lego house!\nThere are no pictures...\nLike\nLiked by 1602 peepers\n#Food\n#Art\n#Creative'
    ])

def test_homepage_delete_peep(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "mousey_14")
    page.fill(".password-tag", "Chitchat981!")
    page.click("text='Log in'")
    page.click("text='Delete'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).not_to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nNothing to peep at...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature'
    ])

def test_top_bar_user_own_page(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    all_lines = page.locator(".top-bar-box-user")
    expect(all_lines).to_have_text("View Profile\nLog out\nson_of_john's Profile")

def test_user_info_user_own_page(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    profile_info = page.locator('.profile-info-box')
    moods = "\ncontent\nexcited\nfabulous\nangry\nlet down\nlucky\nanxious\nworried\nscared\nsad\ncalm\nbuzzing\nhappy\nokay\nbored"
    expect(profile_info).to_have_text('Real name:\nJohnson\nCake day:\n'
                                    '19 October\nCurrent mood:' + moods + '\nLikes to peep at peeps about:\n'
                                    '#DaysOut\n#Food\n#Festivals\nSelect preferred tags\n'
                                    'Account Security:\nChange Password\nDelete Profile')

def test_user_info_other_user_page(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='son_of_john'")
    profile_info = page.locator('.profile-info-box')
    expect(profile_info).to_have_text('Real name:\nJohnson\nCake day:\n'
                                    '19 October\nCurrent mood:\nangry\nLikes to peep at peeps about:\n'
                                    '#DaysOut\n#Food\n#Festivals')

def test_peeps_user_own_page(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    header = page.locator('h2')
    expect(header).to_have_text("son_of_john's Peeps")
    new_peep_button = page.locator('.post-peep-box-button')
    expect(new_peep_button).to_have_text('Post a new peep')
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        f'son_of_john\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n25 December at 07:00\nMerry Christmas everyone!\nThere are no pictures...\nLike\nLiked by 12 peepers\n#Travel',
        f'son_of_john\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n28 September at 14:15\nA perfect day for a picnic.\nThere are no pictures...\nLike\nReady for peeping\n#DaysOut\n#Food\n#Nature',
        f"son_of_john\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 August at 20:46\nIt's a brilliant day for the beach.\nThere are no pictures...\nLike\nLiked by 2 peepers\n#DaysOut"
    ])

def test_peeps_other_user_page(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='son_of_john'")
    header = page.locator('h2')
    expect(header).to_have_text("son_of_john's Peeps")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        f'son_of_john\n25 December at 07:00\nMerry Christmas everyone!\nThere are no pictures...\nLiked\nLiked by 12 peepers\n#Travel',
        f'son_of_john\n28 September at 14:15\nA perfect day for a picnic.\nThere are no pictures...\nLike\nReady for peeping\n#DaysOut\n#Food\n#Nature',
        f"son_of_john\n10 August at 20:46\nIt's a brilliant day for the beach.\nThere are no pictures...\nLiked\nLiked by 2 peepers\n#DaysOut"
    ])

def test_user_own_page_change_mood(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    page.select_option("select[name=mood]", value='5')
    page.click("text='Log out'")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='sammy1890'")
    mood = page.locator(".profile-mood-tag")
    expect(mood).to_have_text('Current mood:\nlet down')
    page.click("text='View Profile'")
    page.select_option("select[name=mood]", value='14')
    page.click("text='Log out'")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='son_of_john'")
    mood = page.locator(".profile-mood-tag")
    expect(mood).to_have_text('Current mood:\nokay')

def test_user_own_page_select_preferred_tags(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    page.click("text='Select preferred tags'")
    keys_to_check = [7, 11]
    for key in keys_to_check:
        checkbox_selector = f'#amend-u-t-box #tag{key}'
        page.check(checkbox_selector)
    page.uncheck('#amend-u-t-box #tag2')
    page.click("text='Confirm'")
    profile_info = page.locator('.profile-info-box')
    moods = "\ncontent\nexcited\nfabulous\nangry\nlet down\nlucky\nanxious\nworried\nscared\nsad\ncalm\nbuzzing\nhappy\nokay\nbored"
    expect(profile_info).to_have_text('Real name:\nJohnson\nCake day:\n'
                                    '19 October\nCurrent mood:' + moods + '\nLikes to peep at peeps about:\n'
                                    '#DaysOut\n#Festivals\n#Art\n#Creative\nSelect preferred tags\n'
                                    'Account Security:\nChange Password\nDelete Profile')
    
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
    page.click("text='Change Password'")
    page.fill("#old_password", "Never0!")
    page.fill("#new_password", "akfjs")
    page.fill("#c_new_password", "akfjs")
    page.click("text='Lock Securely'")
    error = page.locator(".cp_error")
    expect(error).to_have_text("Old password did not match!")
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

def test_user_page_add_peep_successful(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    page.click("text='Post a new peep'")
    page.fill(".comment-box", "This is a new peep.")
    keys_to_check = [1, 3]
    for key in keys_to_check:
        checkbox_selector = f'.tag-to-select-box >> #tag{key}'
        page.check(checkbox_selector)
    page.click("text='Post that peep!'")
    month, day, hour, minute = add_zero(datetime.now().month), add_zero(datetime.now().day), add_zero(datetime.now().hour), add_zero(datetime.now().minute)
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        f'son_of_john\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n{day} {months[int(month)]} at {hour}:{minute}\nThis is a new peep.\nThere are no pictures...\nLike\nReady for peeping\n#DaysOut\n#Travel',
        f'son_of_john\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n25 December at 07:00\nMerry Christmas everyone!\nThere are no pictures...\nLike\nLiked by 12 peepers\n#Travel',
        f'son_of_john\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n28 September at 14:15\nA perfect day for a picnic.\nThere are no pictures...\nLike\nReady for peeping\n#DaysOut\n#Food\n#Nature',
        f"son_of_john\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n10 August at 20:46\nIt's a brilliant day for the beach.\nThere are no pictures...\nLike\nLiked by 2 peepers\n#DaysOut"
    ])

def test_user_page_add_peep_error(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    page.click("text='Post a new peep'")
    page.click("text='Post that peep!'")
    error = page.locator(".peep_error")
    expect(error).to_have_text("Peeps need literate or visual content!")

def test_other_user_page_click_peep_at_images(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='mousey_14'")
    page.click("text='Peep at the pictures'")
    pop_up_box = page.locator('.picture-peep-box')
    expect(pop_up_box).to_have_text('mousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.')

def test_other_user_page_click_like(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='mousey_14'")
    page.click("text='Like'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLiked\nLiked by 45331 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        'mousey_14\n31 August at 18:52\nDelicious 4 cheese pizza I made!\nThere are no pictures...\nLike\nLiked by 24 peepers\n#Food\n#Hobbies\n#Art'
    ])

def test_other_user_page_click_liked(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='mousey_14'")
    page.click("text='Liked'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLike\nLiked by 55 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        'mousey_14\n31 August at 18:52\nDelicious 4 cheese pizza I made!\nThere are no pictures...\nLike\nLiked by 24 peepers\n#Food\n#Hobbies\n#Art'
    ])

def test_own_user_page_click_amend_tags(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "mousey_14")
    page.fill(".password-tag", "Chitchat981!")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    page.click("text='Amend tags'")
    keys_to_check = [2, 7]
    for key in keys_to_check:
        checkbox_selector = f'#amend-p-t-box-15 #tag{key}'
        page.check(checkbox_selector)
    page.uncheck('#amend-p-t-box-15 #tag4')
    page.click("#amend-p-t-box-15 >> text='Confirm'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        f'mousey_14\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n30 May at 17:59\nKayaking at the lake.\nThere are no pictures...\nLike\nLiked by 56 peepers\n#DaysOut\n#Food\n#Art\n#Nature',
        f'mousey_14\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'mousey_14\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n31 August at 18:52\nDelicious 4 cheese pizza I made!\nThere are no pictures...\nLiked\nLiked by 24 peepers\n#Food\n#Hobbies\n#Art'
    ])

def test_own_user_page_click_delete_peep(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "mousey_14")
    page.fill(".password-tag", "Chitchat981!")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    page.click("text='Delete'")
    page.click("#delete-peep-box-15 >> text='Confirm'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_have_text([
        f'mousey_14\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        f'mousey_14\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n31 August at 18:52\nDelicious 4 cheese pizza I made!\nThere are no pictures...\nLiked\nLiked by 24 peepers\n#Food\n#Hobbies\n#Art'
    ])