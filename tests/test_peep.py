from lib.peep import Peep
from datetime import datetime

def test_peep_constructs():
    timestamp_value = '2022-08-31 18:52:58'
    datetime_object = datetime.strptime(timestamp_value, '%Y-%m-%d %H:%M:%S')
    tags = [7, 8, 11]
    images = [6, 7, 8]
    peep = Peep(19, "I painted a picture of the lake.", datetime_object, 15, 3, tags, images)
    assert peep.id == 19
    assert peep.content == "I painted a picture of the lake."
    assert peep.time == datetime_object
    assert peep.likes == 15
    assert peep.user_id == 3
    assert peep.tags == [7, 8, 11]
    assert peep.images == [6, 7, 8]