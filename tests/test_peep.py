from lib.peep import *
from datetime import datetime

def test_peep_constructs():
    timestamptz_value = '2022-08-31 18:52:58'
    datetime_object = datetime.strptime(timestamptz_value, '%Y-%m-%d %H:%M:%S')
    peep = Peep(19, "I painted a picture of the lake.", datetime_object, 15, 3)
    assert peep.id == 19
    assert peep.content == "I painted a picture of the lake."
    assert peep.time == datetime_object
    assert peep.likes == 15
    assert peep.user_id == 3
