from ChitterApp.lib.models.user import User


def test_user_constructs():
    tags = [1, 5, 10]
    user = User(3, "Sam", "samsuel", "1999/02/27", "content", tags)
    assert user.id == 3
    assert user.name == "Sam"
    assert user.user_name == "samsuel"
    assert user.d_o_b == "1999/02/27"
    assert user.current_mood == "content"
    assert user.tags == [1, 5, 10]


def test_user_instances_are_equal():
    tags = [3, 4, 6, 7, 12]
    user1 = User(3, "Sam", "samsuel", "1999/02/27", "content", tags)
    user2 = User(3, "Sam", "samsuel", "1999/02/27", "content", tags)
    assert user1 == user2
