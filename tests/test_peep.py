from ChitterApp.lib.models.peep import Peep
from datetime import datetime


def test_peep_constructs():
    timestamp_value = '2022-08-31 18:52:58'
    datetime_object = datetime.strptime(timestamp_value, '%Y-%m-%d %H:%M:%S')
    tags = [7, 8, 11]
    images = [6, 7, 8]
    peep = Peep(19, "I painted a picture of the lake.", datetime_object, 15, 3, "bubble_bug", tags, images, True)
    assert peep.id == 19
    assert peep.content == "I painted a picture of the lake."
    assert peep.time == datetime(2022, 8, 31, 18, 52, 58)
    assert peep.likes == 15
    assert peep.user_id == 3
    assert peep.user_name == "bubble_bug"
    assert peep.tags == [7, 8, 11]
    assert peep.images == [6, 7, 8]
    assert peep.user_likes == True


def test_peep_instances_are_equal():
    timestamp_value = '2022-08-31 18:52:58'
    datetime_object = datetime.strptime(timestamp_value, '%Y-%m-%d %H:%M:%S')
    tags = [7, 8, 11]
    images = [6, 7, 8]
    peep1 = Peep(19, "I painted a picture of the lake.", datetime_object, 15, 3, "bubble_bug", tags, images, True)
    peep2 = Peep(19, "I painted a picture of the lake.", datetime_object, 15, 3, "bubble_bug", tags, images, True)
    assert peep1 == peep2
