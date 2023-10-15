from lib.user_repository import UserRepository
from lib.user import User
import datetime

def test_get_all_users(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = UserRepository(db_connection)
    assert repo.get_all() == [
        User(1, 'Jody', 'jodesnode', 'Pass123!', datetime.date(1993, 8, 6), 'calm', [1, 3, 5]),
        User(2, 'Sam', 'sammy1890', 'Word234*', datetime.date(1999, 2, 27), 'excited', [2, 4]),
        User(3, 'Johnson', 'son_of_john', 'Never00!', datetime.date(1995, 10, 19), 'angry', [1, 2, 5]),
        User(4, 'Alice', 'mousey_14', 'Chitchat981!', datetime.date(1982, 5, 31), 'content', [1, 3, 4]),
        User(5, 'Rose', 'rosy_red', 'gatheR&45', datetime.date(1993, 5, 15), 'calm', [5])
    ]

def test_get_all_user_names(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = UserRepository(db_connection)
    assert repo.get_all_user_names() == ['jodesnode', 'sammy1890', 'son_of_john', 'mousey_14', 'rosy_red']

def test_find_by_id(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = UserRepository(db_connection)
    assert repo.find_by_id(4) == User(4, 'Alice', 'mousey_14', 'Chitchat981!',
                                    datetime.date(1982, 5, 31), 'content', [1, 3, 4])
    assert repo.find_by_id(6) == None

def test_find_by_user_name(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = UserRepository(db_connection)
    assert repo.find_by_user_name('son_of_john') == User(3, 'Johnson', 'son_of_john', 'Never00!',
                                                        datetime.date(1995, 10, 19), 'angry', [1, 2, 5])
    assert repo.find_by_user_name('moon15') == None

def test_check_valid_password(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = UserRepository(db_connection)
    assert repo.check_valid_password('sunny') == ['Password must be at least 8 characters.',
                                                'Password must contain uppercase and lowercase characters.',
                                                'Password must contain at least 1 number.',
                                                'Password must contain at least 1 symbol.']
    assert repo.check_valid_password('Mighty7') == ['Password must be at least 8 characters.',
                                                    'Password must contain at least 1 symbol.']
    assert repo.check_valid_password('Io983&!') == ['Password must be at least 8 characters.']
    assert repo.check_valid_password('POIAHD*&^231') == ['Password must contain uppercase and lowercase characters.']
    assert repo.check_valid_password('ankfsahou*&^231') == ['Password must contain uppercase and lowercase characters.']
    assert repo.check_valid_password('Almighty3!') == True
    assert repo.check_valid_password('1938>John') == True

def test_check_valid_d_o_b(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = UserRepository(db_connection)
    assert repo.check_valid_d_o_b([16, 'July', 1988]) == True
    assert repo.check_valid_d_o_b([31, 'June', 1995]) == "June only has 30 days!"
    assert repo.check_valid_d_o_b([30, 'February', 2001]) == "February only has 28 or 29 days!"
    assert repo.check_valid_d_o_b([31, 'November', 1956]) == "November only has 30 days!"
    assert repo.check_valid_d_o_b([31, 'December', 1999]) == True
    assert repo.check_valid_d_o_b([29, 'February', 2004]) == True
    assert repo.check_valid_d_o_b([29, 'February', 2005]) == "February only had 28 days in 2005!"

def test_add_new_user(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = UserRepository(db_connection)
    assert repo.add_user('Tim', 'timmy1989', 'Password123!', 'Password123!', [31, 'December', 1989]) == 6
    assert repo.add_user('Sally', 'salzsy', 'sdgafga', 'ewtrewte', [31, 'July', 1976]) == {
                        'password':['Password must be at least 8 characters.',
                                    'Password must contain uppercase and lowercase characters.',
                                    'Password must contain at least 1 number.',
                                    'Password must contain at least 1 symbol.'],
                        'pws_match':'Passwords do not match!'}
    assert repo.add_user('', 'big_bold_tree', 'Petal123$', 'Petal123$', [2, 'June', 2005]) == {
        'name':'Please provide a name!'}
    assert repo.add_user('Sam', '', 'P@ker827', 'P@ker827', [14, 'March', 2010]) == {
        'user_name':'Please choose a username!'}
    assert repo.add_user('Sam', 'sammy1890', 'P@ker827', 'P@ker827', [1, 'January', 2000]) == {
        'user_name':'Username taken!'}
    assert repo.add_user('Thomas Jones', 'jonsy19', 'rudE<b0y', 'rudE<b0', [2, 'June', 2005]) == {
        'pws_match':'Passwords do not match!'}
    assert repo.add_user('Thomas Jones', 'jonsy19', 'rudE<b0', 'rudE<b0y', [2, 'June', 2005]) == {
        'password':['Password must be at least 8 characters.'],
        'pws_match':'Passwords do not match!'}
    assert repo.add_user('Thomas Jones', 'jonsy19', 'rudE<b0y', 'rudE<b0i', [2, 'June', 2005]) == {
        'pws_match':'Passwords do not match!'}
    assert repo.add_user('', 'jonsy19', 'rudE<b0y', 'rudE<b0', [2, 'June', 2005]) == {
        'name':'Please provide a name!',
        'pws_match':'Passwords do not match!'}
    assert repo.add_user('Sam', 'simsual', 'P@ker827', 'P@ker827', [31, 'September', 2010]) == {
        'date':'September only has 30 days!'}
    assert repo.add_user('Sam', 'simsual', 'P@ker827', 'P@ker827', [31, 'February', 2010]) == {
        'date':"February only has 28 or 29 days!"}
    assert repo.add_user('Sam', 'simsual', 'P@ker827', 'P@ker827', [29, 'February', 2010]) == {
        'date':"February only had 28 days in 2010!"}
    assert repo.add_user('Sam', 'simsual', 'P@ker827', 'P@ker827', [28, 'February', 2010]) == 7
    assert repo.add_user('', '', '', '', [3, 'April', 2004]) == {
        'name':'Please provide a name!',
        'user_name':'Please choose a username!',
        'password':['Password must be at least 8 characters.',
                    'Password must contain uppercase and lowercase characters.',
                    'Password must contain at least 1 number.',
                    'Password must contain at least 1 symbol.']
    }
    assert repo.get_all() == [
        User(1, 'Jody', 'jodesnode', 'Pass123!', datetime.date(1993, 8, 6), 'calm', [1, 3, 5]),
        User(2, 'Sam', 'sammy1890', 'Word234*', datetime.date(1999, 2, 27), 'excited', [2, 4]),
        User(3, 'Johnson', 'son_of_john', 'Never00!', datetime.date(1995, 10, 19), 'angry', [1, 2, 5]),
        User(4, 'Alice', 'mousey_14', 'Chitchat981!', datetime.date(1982, 5, 31), 'content', [1, 3, 4]),
        User(5, 'Rose', 'rosy_red', 'gatheR&45', datetime.date(1993, 5, 15), 'calm', [5]),
        User(6, 'Tim', 'timmy1989', 'Password123!', datetime.date(1989, 12, 31), 'content', []),
        User(7, 'Sam', 'simsual', 'P@ker827', datetime.date(2010, 2, 28), 'content', [])
    ]

def test_user_name_password_match(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = UserRepository(db_connection)
    assert repo.user_name_password_match('jodesnode', 'Pass123!') == 1
    assert repo.user_name_password_match('mousey_14', 'Chitchat981!') == 4
    assert repo.user_name_password_match('windy_file', 'Chitchat981!') == "Username does not exist."
    assert repo.user_name_password_match('rosy_red', 'petter&%14!') == "Incorrect password."
    assert repo.user_name_password_match('rosy_red', 'Chitchat981!') == "Incorrect password."
    assert repo.user_name_password_match('rosy_red', 'gatheR&45') == 5

def test_update_user(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = UserRepository(db_connection)
    assert repo.update(4, current_mood="calm") == None
    assert repo.find_by_id(4) == User(4, 'Alice', 'mousey_14', 'Chitchat981!',
                                    datetime.date(1982, 5, 31), 'calm', [1, 3, 4])
    assert repo.update(3, password="br@Ker21", confirm_password="br@Ker21") == None
    assert repo.find_by_user_name('son_of_john') == User(3, 'Johnson', 'son_of_john', 'br@Ker21',
                                                        datetime.date(1995, 10, 19), 'angry', [1, 2, 5])
    assert repo.update(4, password="82719", confirm_password="82719") == [
        'Password must be at least 8 characters.',
        'Password must contain uppercase and lowercase characters.',
        'Password must contain at least 1 symbol.'
    ]
    assert repo.update(4, password="Fantastic!", confirm_password="Fantastic!") == [
        'Password must contain at least 1 number.'
    ]
    assert repo.find_by_id(4) == User(4, 'Alice', 'mousey_14', 'Chitchat981!',
                                    datetime.date(1982, 5, 31), 'calm', [1, 3, 4])
    assert repo.update(2, password="hero", confirm_password="4") == [
        'Password must be at least 8 characters.',
        'Password must contain uppercase and lowercase characters.',
        'Password must contain at least 1 number.',
        'Password must contain at least 1 symbol.'
    ]
    assert repo.update(2, password="hero", confirm_password="Mental*>@15") == [
        'Password must be at least 8 characters.',
        'Password must contain uppercase and lowercase characters.',
        'Password must contain at least 1 number.',
        'Password must contain at least 1 symbol.'
    ]
    assert repo.update(4, password="", confirm_password="") == [
        'Password must be at least 8 characters.',
        'Password must contain uppercase and lowercase characters.',
        'Password must contain at least 1 number.',
        'Password must contain at least 1 symbol.'
    ]
    assert repo.update(5, password="Mental*>@15", confirm_password="hero") == 'Passwords do not match!'
    assert repo.update(1, password="Mental*>@15", confirm_password="Mentsl*>@15") == 'Passwords do not match!'
    assert repo.update(1, password="Mental*>@15", confirm_password="Mental*>@15") == None
    assert repo.get_all() == [
        User(1, 'Jody', 'jodesnode', 'Mental*>@15', datetime.date(1993, 8, 6), 'calm', [1, 3, 5]),
        User(2, 'Sam', 'sammy1890', 'Word234*', datetime.date(1999, 2, 27), 'excited', [2, 4]),
        User(3, 'Johnson', 'son_of_john', 'br@Ker21', datetime.date(1995, 10, 19), 'angry', [1, 2, 5]),
        User(4, 'Alice', 'mousey_14', 'Chitchat981!', datetime.date(1982, 5, 31), 'calm', [1, 3, 4]),
        User(5, 'Rose', 'rosy_red', 'gatheR&45', datetime.date(1993, 5, 15), 'calm', [5])
    ]

def test_delete_user(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = UserRepository(db_connection)
    assert repo.delete(3, 'Never00!') == None
    assert repo.get_all() == [
        User(1, 'Jody', 'jodesnode', 'Pass123!', datetime.date(1993, 8, 6), 'calm', [1, 3, 5]),
        User(2, 'Sam', 'sammy1890', 'Word234*', datetime.date(1999, 2, 27), 'excited', [2, 4]),
        User(4, 'Alice', 'mousey_14', 'Chitchat981!', datetime.date(1982, 5, 31), 'content', [1, 3, 4]),
        User(5, 'Rose', 'rosy_red', 'gatheR&45', datetime.date(1993, 5, 15), 'calm', [5])
    ]
    assert repo.delete(2, 'sammy 1990') == "Incorrect password."
    assert repo.delete(4, 'Chitchat981!') == None
    assert repo.get_all() == [
        User(1, 'Jody', 'jodesnode', 'Pass123!', datetime.date(1993, 8, 6), 'calm', [1, 3, 5]),
        User(2, 'Sam', 'sammy1890', 'Word234*', datetime.date(1999, 2, 27), 'excited', [2, 4]),
        User(5, 'Rose', 'rosy_red', 'gatheR&45', datetime.date(1993, 5, 15), 'calm', [5])
    ]
