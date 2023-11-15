from playwright.sync_api import expect
from datetime import datetime
from ChitterApp.constants import add_zero, months
import os
os.environ['REDIS_TIMEOUT'] = '1'


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


select_tags_box = "×\nSelect Tags for Peep\n#DaysOut\n#Food\n#Travel\n#Hobbies\n#Festivals\n#Music"\
                "\n#Art\n#Nature\n#Social\n#Work\n#Creative\n#Books\nConfirm"
delete_box = "Are you sure you want to delete this peep?\nConfirm\nCancel"


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
    page.wait_for_timeout(1000)
    page.select_option("select[name=mood]", value='5')
    page.click("text='Log out'")
    page.fill(".user-name-tag", "son_of_john")
    page.fill(".password-tag", "Never00!")
    page.click("text='Log in'")
    page.click("text='sammy1890'")
    mood = page.locator(".profile-mood-tag")
    expect(mood).to_have_text('Current mood:\nlet down')
    page.click("text='View Profile'")
    page.wait_for_timeout(1000)
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
                                    '#DaysOut\n#Creative\n#Festivals\n#Art\nSelect preferred tags\n'
                                    'Account Security:\nChange Password\nDelete Profile')


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


def test_user_page_add_peep_bad_words(page, test_web_address, db_connection):
    db_connection.seed("seeds/chitter_data.sql")
    page.goto(f"http://{test_web_address}")
    page.fill(".user-name-tag", "sammy1890")
    page.fill(".password-tag", "Word234*")
    page.click("text='Log in'")
    page.click("text='View Profile'")
    page.click("text='Post a new peep'")
    page.fill(".comment-box", "Let's go to a hornet farm!")
    page.click("text='Post that peep!'")
    error = page.locator(".peep_error")
    expect(error).to_have_text("The word(s) 'hornet' is not allowed in peeps!")
    page.click("text='Post a new peep'")
    page.fill(".comment-box", "The UK Home Office are wonderful! Not!")
    page.click("text='Post that peep!'")
    error = page.locator(".peep_error")
    expect(error).to_have_text("The word(s) 'home office' is not allowed in peeps!")
    page.click("text='Post a new peep'")
    page.fill(".comment-box", "Scotch eggs are amazing for breakfast.")
    page.click("text='Post that peep!'")
    error = page.locator(".peep_error")
    expect(error).to_have_text("The word(s) 'scotch egg' is not allowed in peeps!")


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
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLiked\nLiked by 45331 peepers\n#Creative\n#Travel\n#Hobbies\n#Art\n#Nature',
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
        'mousey_14\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Creative\n#Travel\n#Hobbies\n#Art\n#Nature',
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
        f'mousey_14\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Creative\n#Travel\n#Hobbies\n#Art\n#Nature',
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
        f'mousey_14\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n30 May at 11:02\nA picture I painted in Turkey.\nPeep at the pictures\nmousey_14\n30 May at 11:02\n×\nA picture I painted in Turkey.\nLike\nLiked by 45330 peepers\n#Creative\n#Travel\n#Hobbies\n#Art\n#Nature',
        f'mousey_14\nAmend tags\n{select_tags_box}\nDelete\n{delete_box}\n31 August at 18:52\nDelicious 4 cheese pizza I made!\nThere are no pictures...\nLiked\nLiked by 24 peepers\n#Food\n#Hobbies\n#Art'
    ])
