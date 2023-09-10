from lib.user import User

def test_user_constructs():
    user = User(3, "Sam", "samsuel", "Norder432$", "1999/02/27", "content")
    assert user.id == 3
    assert user.name == "Sam"
    assert user.user_name == "samsuel"
    assert user.password == "Norder432$"
    assert user.d_o_b == "1999/02/27"
    assert user.current_mood == "content"

def test_user_instances_are_equal():
    user1 = User(3, "Sam", "samsuel", "Norder432$", "1999/02/27", "content")
    user2 = User(3, "Sam", "samsuel", "Norder432$", "1999/02/27", "content")
    assert user1 == user2
