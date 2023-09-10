from playwright.sync_api import Page, expect
from datetime import datetime
from freezegun import freeze_time

@freeze_time("2023-09-07 12:00:01")
def test_time():
    assert datetime.now() == datetime(2023, 9, 7, 12, 0, 1)

def test_top_bar_homepage_unauthenticated(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    user_name_card = page.locator(".user_name-card")
    placeholder_value = user_name_card.get_attribute("placeholder")
    assert placeholder_value == 'Username'
    password_card = page.locator(".password-card")
    placeholder_value = password_card.get_attribute("placeholder")
    assert placeholder_value == 'Password'
    top_bar_button = page.locator(".top-bar-button")
    expect(top_bar_button).to_have_text(['Log in', 'Sign up'])
    not_member_text = page.locator(".not_member-text")
    expect(not_member_text).to_have_text('Not a member?')

def test_peeps_homepage_unauthenticated(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nNothing to peep at...\nLike\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at 1 portrayal\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        'sammy1890\n10 February at 19:45\nMy fantastic lego house!\nNothing to peep at...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def test_homepage_unauthenticated_click_user_name(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='jodesnode'")
    authentication = page.locator(".authentication")
    expect(authentication).to_have_text("Log in or sign up to view user profiles!")

def test_homepage_unauthenticated_click_like(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Like'")
    authentication = page.locator(".authentication")
    expect(authentication).to_have_text("Log in or sign up to like others' peeps!")

def test_homepage_unauthenticated_click_peep_at_images(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Peep at 1 portrayal'")
    pop_up_box = page.locator('.centered-box')  # LIKELY TO CHANGE !!!!!
    expect(pop_up_box).to_have_text('X\nmousey_14\nLike\nLiked by 45330 peepers\nA picture I painted in Turkey.')

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
    success = page.locator(".success")
    expect(success).to_have_text("Welcome to your Chitter, parker89!")

def test_sign_up_page_sign_up_no_input(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Sign up'")
    page.click("text='Confirm & sign up'")
    errors = page.locator(".error")
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
    error = page.locator(".error")
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
    error = page.locator(".error")
    expect(error).to_have_text("Passwords do not match!")

def test_log_in_login_in_successful(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "son_of_john")
    page.fill(".password-card", "Never00!")
    page.click("text='Log in'")
    success = page.locator(".success")
    expect(success).to_have_text("Welcome to your Chitter, son_of_john!")

def test_log_in_login_in_no_input(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.click("text='Log in'")
    error = page.locator(".error")
    expect(error).to_have_text("Enter your username and password.")

def test_log_in_login_in_no_password(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "son_of_john")
    page.click("text='Log in'")
    error = page.locator(".error")
    expect(error).to_have_text("Enter your password.")

def test_log_in_login_in_no_user_name(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".password-card", "Never00!")
    page.click("text='Log in'")
    error = page.locator(".error")
    expect(error).to_have_text("Enter your username.")

def test_log_in_login_in_incorrect_password(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "son_of_john")
    page.fill(".password-card", "Never001")
    page.click("text='Log in'")
    error = page.locator(".error")
    expect(error).to_have_text("Incorrect password. Please try again.")

def test_log_in_login_in_user_name_does_not_exist(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "son_of_kate")
    page.fill(".password-card", "Never00*")
    page.click("text='Log in'")
    error = page.locator(".error")
    expect(error).to_have_text("Username does not exist. Please try again.")

def test_top_bar_homepage_authenticated(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "son_of_john")
    page.fill(".password-card", "Never00!")
    page.click("text='Log in'")
    all_lines = page.locator(".top-bar")
    tags = "\nAll tags\n#DaysOut\n#Food\n#Travel\n#Hobbies\n#Festivals\n#Music\n#Art\n#Nature\n#Social\n#Work\n#Creative\n#Books"
    moods = "\ncontent\nexcited\nfabulous\nangry\nlet down\nlucky\nanxious\nworried\nscared\nsad\ncalm\nbuzzing\nhappy\nokay\nbored"
    expect(all_lines).to_have_text('Viewing:' + tags + '\nMood:' + moods + '\nson_of_john\nView Profile\nLog out')

def test_peeps_homepage_authenticated(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "sammy1890")
    page.fill(".password-card", "Word234*")
    page.click("text='Log in'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nNothing to peep at...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at 1 portrayal\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        'sammy1890\nAmend tags\nDelete\n10 February at 19:45\nMy fantastic lego house!\nNothing to peep at...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def add_zero(number):
    if len(str(number)) == 1:
        return f"0{number}"
    return str(number)

def test_homepage_add_peep_successful(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "sammy1890")
    page.fill(".password-card", "Word234*")
    page.click("text='Log in'")
    page.fill(".comment_box", "This is a new peep.")
    keys_to_check = [1, 3]
    for key in keys_to_check:
        checkbox_selector = f'#tag{key}'
        page.check(checkbox_selector)
    page.click("text='Peep-it'")
    day, hour, minute = add_zero(datetime.now().day), add_zero(datetime.now().hour), add_zero(datetime.now().minute)
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        f'sammy1890\nAmend tags\nDelete\n{day} September at {hour}:{minute}\nThis is a new peep.\nNothing to peep at...\nLike\nReady for peeping\n#DaysOut\n#Travel',
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nNothing to peep at...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at 1 portrayal\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        'sammy1890\nAmend tags\nDelete\n10 February at 19:45\nMy fantastic lego house!\nNothing to peep at...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def test_homepage_add_peep_error(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "sammy1890")
    page.fill(".password-card", "Word234*")
    page.click("text='Log in'")
    page.click("text='Peep-it'")
    error = page.locator(".error")
    expect(error).to_have_text("There's nothing to peep at here!")

def test_homepage_authenticated_click_user_name(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "sammy1890")
    page.fill(".password-card", "Word234*")
    page.click("text='Log in'")
    page.click("text='jodesnode'")
    header = page.locator('h1')
    expect(header).to_have_text('User Profile')
    profile_info = page.locator('.profile_info-tag')
    expect(profile_info).to_have_text('Username:\njodesnode\nReal name:\nJody\nDate of birth:\n'
                                    '06 August 1993\nCurrent mood:\ncalm\nLikes to peep at peeps about:\n'
                                    '#DaysOut\n#Travel\n#Festivals')
    header = page.locator('h2')
    expect(header).to_have_text("jodesnode's Peeps")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'jodesnode\n01 January at 00:04\nHappy New Year from South Korea!\nNothing to peep at...\nLiked\nLiked by 130 peepers\n#Travel\n#Festivals',
        'jodesnode\n23 August at 10:02\nPhotos from my holiday in spain.\nNothing to peep at...\nLike\nLiked by 10 peepers\n#Travel\n#Nature',
        'jodesnode\n10 August at 19:10\nI went to Summerfield park today.\nNothing to peep at...\nLike\nLiked by 4 peepers\n#DaysOut\n#Nature'
    ])

def test_homepage_authenticated_click_like_and_liked(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "sammy1890")
    page.fill(".password-card", "Word234*")
    page.click("text='Log in'")
    page.click("text='Like'")
    page.click("text='Liked'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nNothing to peep at...\nLike\nLiked by 55 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at 1 portrayal\nLiked\nLiked by 45331 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        'sammy1890\nAmend tags\nDelete\n10 February at 19:45\nMy fantastic lego house!\nNothing to peep at...\nLike\nLiked by 1602 peepers\n#Hobbies\n#Creative'
    ])

def test_homepage_authenticated_click_peep_at_images(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "sammy1890")
    page.fill(".password-card", "Word234*")
    page.click("text='Log in'")
    page.click("text='Peep at 1 portrayal'")
    pop_up_box = page.locator('.centered-box')  # LIKELY TO CHANGE !!!!!
    expect(pop_up_box).to_have_text('X\nmousey_14\nLike\nLiked by 45330 peepers\nA picture I painted in Turkey.')
    page.click('.centered-box >> button:has-text("Like")')  # LIKELY TO CHANGE !!!!!
    expect(pop_up_box).to_have_text('X\nmousey_14\nLiked\nLiked by 45331 peepers\nA picture I painted in Turkey.')
    page.click('.centered-box >> a:has-text("mousey_14")')  # LIKELY TO CHANGE !!!!!
    header = page.locator('h1')
    expect(header).to_have_text('User Profile')
    profile_info = page.locator('.profile_info-tag')
    expect(profile_info).to_have_text('Username:\nmousey_14\nReal name:\nAlice\nDate of birth:\n'
                                    '31 May 1982\nCurrent mood:\ncontent\nLikes to peep at peeps about:\n'
                                    '#DaysOut\n#Travel\n#Hobbies')
    header = page.locator('h2')
    expect(header).to_have_text("mousey_14's Peeps")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nNothing to peep at...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nLiked\nLiked by 45331 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        'mousey_14\n31 August at 18:52\nDelicious 4 cheese pizza I made!\nNothing to peep at...\nLike\nLiked by 24 peepers\n#Food\n#Hobbies\n#Art'
    ])

def test_homepage_click_amend_tags(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "sammy1890")
    page.fill(".password-card", "Word234*")
    page.click("text='Log in'")
    page.click("text='Amend tags'")
    keys_to_check = [2, 7]
    for key in keys_to_check:
        checkbox_selector = f'#tag{key}'
        page.check(checkbox_selector)
    page.uncheck('#tag4')
    page.click("text='Confirm'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nNothing to peep at...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature',
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at 1 portrayal\nLike\nLiked by 45330 peepers\n#Travel\n#Hobbies\n#Art\n#Nature\n#Creative',
        'sammy1890\nAmend tags\nDelete\n10 February at 19:45\nMy fantastic lego house!\nNothing to peep at...\nLike\nLiked by 1602 peepers\n#Food\n#Art\n#Creative'
    ])

def test_homepage_delete_peep(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user_name-card", "mousey_14")
    page.fill(".password-card", "Chitchat981!")
    page.click("text='Log in'")
    page.click("text='Delete'")
    all_lines = page.locator(".peep-container")
    expect(all_lines).not_to_contain_text([
        'mousey_14\n30 May at 17:59\nKayaking at the lake.\nNothing to peep at...\nLiked\nLiked by 56 peepers\n#DaysOut\n#Hobbies\n#Nature'
    ])
