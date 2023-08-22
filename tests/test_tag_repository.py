from lib.tag_repository import *

def test_get_all_tags(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = TagRepository(db_connection)
    assert repo.get_all() == {1: '#DaysOut', 2: '#Food', 3: '#Travel', 4: '#Hobbies',
                            5: '#Festivals', 6: '#Music', 7: '#Art', 8: '#Nature',
                            9: '#Social', 10: '#Work', 11: '#Creative', 12: '#Books'}

def test_does_user_favour_tag(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = TagRepository(db_connection)
    assert repo.does_user_favour_tag(1, 5) == True
    assert repo.does_user_favour_tag(3, 5) == True
    assert repo.does_user_favour_tag(4, 5) == False
    assert repo.does_user_favour_tag(5, 10) == False

def test_add_tag_to_user(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = TagRepository(db_connection)
    assert repo.add_tag_to_user(4, 4) == "Already connected!"
    assert repo.does_user_favour_tag(1, 8) == False
    assert repo.add_tag_to_user(1, 8) == None
    assert repo.does_user_favour_tag(1, 8) == True
    assert repo.add_tag_to_user(1, 8) == "Already connected!"
    assert repo.does_user_favour_tag(4, 12) == False
    assert repo.add_tag_to_user(4, 12) == None
    assert repo.does_user_favour_tag(4, 12) == True

def test_remove_tag_from_user(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = TagRepository(db_connection)
    assert repo.remove_tag_from_user(4, 11) == "Was not connected in the first place!"
    assert repo.does_user_favour_tag(4, 4) == True
    assert repo.remove_tag_from_user(4, 4) == None
    assert repo.does_user_favour_tag(4, 4) == False
    assert repo.does_user_favour_tag(3, 2) == True
    assert repo.remove_tag_from_user(3, 2) == None
    assert repo.does_user_favour_tag(3, 2) == False

def test_add_tag_to_peep(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = TagRepository(db_connection)
    assert repo.add_tag_to_peep(12, 2) == None
    assert repo.add_tag_to_peep(12, 2) == "Already connected!"
    assert repo.add_tag_to_peep(4, 10) == None
    assert repo.add_tag_to_peep(4, 10) == "Already connected!"
    assert repo.add_tag_to_peep(1, 1) == "Already connected!"
    assert repo.add_tag_to_peep(14, 11) == "Already connected!"

def test_remove_tag_from_peep(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = TagRepository(db_connection)
    assert repo.remove_tag_from_peep(1, 1) == None
    assert repo.remove_tag_from_peep(1, 1) == "Was not connected in the first place!"
    assert repo.remove_tag_from_peep(13, 4) == None
    assert repo.remove_tag_from_peep(13, 4) == "Was not connected in the first place!"
    assert repo.remove_tag_from_peep(2, 1) == "Was not connected in the first place!"
    assert repo.remove_tag_from_peep(9, 5) == "Was not connected in the first place!"

def test_get_users_tags(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = TagRepository(db_connection)
    assert repo.get_users_tags(4) == {1: '#DaysOut', 3: '#Travel', 4: '#Hobbies'}
    assert repo.get_users_tags(2) == {2: '#Food', 4: '#Hobbies'}
    assert repo.get_users_tags(5) == {5: '#Festivals'}

def test_get_peeps_tags(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = TagRepository(db_connection)
    assert repo.get_peeps_tags(6) == {2: '#Food', 4: '#Hobbies', 7: '#Art'}
    assert repo.get_peeps_tags(13) == {4: '#Hobbies', 11: '#Creative'}
    assert repo.get_peeps_tags(7) == {4: '#Hobbies', 12: '#Books'}
