from ChitterApp.lib.repositories.peep_repository import PeepRepository
from ChitterApp.lib.models.peep import Peep
from datetime import datetime
from freezegun import freeze_time

def test_get_all_peeps(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.get_all() == [
        Peep(15, 'Kayaking at the lake.', datetime(2023, 5, 30, 17, 59, 4), 56, 4, [1, 4, 8], []),
        Peep(14, 'A picture I painted in Turkey.', datetime(2023, 5, 30, 11, 2, 59), 45330, 4, [3, 4, 7, 8, 11], [1]),
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, [4, 11], []),
        Peep(12, 'Party at mine tonight!', datetime(2023, 1, 15, 16, 35, 50), 3, 5, [6, 9], []),
        Peep(11, 'Happy New Year from South Korea!', datetime(2023, 1, 1, 0, 4, 56), 130, 1, [3, 5], []),
        Peep(10, 'Merry Christmas everyone!', datetime(2022, 12, 25, 7, 0, 1), 12, 3, [3], []),
        Peep(9, 'A perfect day for a picnic.', datetime(2022, 9, 28, 14, 15, 24), 0, 3, [1, 2, 8], []),
        Peep(8, 'Italy is a brilliant place to visit!', datetime(2022, 9, 27, 23, 49, 14), 4, 5, [3], []),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, [4, 12], []),
        Peep(6, 'Delicious 4 cheese pizza I made!', datetime(2022, 8, 31, 18, 52, 58), 24, 4, [2, 4, 7], []),
        Peep(5, 'Photos from my holiday in spain.', datetime(2022, 8, 23, 10, 2, 3), 10, 1, [3, 8], []),
        Peep(4, 'Who wants to go for food tonight?', datetime(2022, 8, 11, 15, 22, 33), 5, 2, [2, 9], []),
        Peep(3, "It's a brilliant day for the beach.", datetime(2022, 8, 10, 20, 46, 40), 2, 3, [1], []),
        Peep(2, 'This ice cream is amazing!', datetime(2022, 8, 10, 19, 25, 6), 7, 2, [2], []),
        Peep(1, 'I went to Summerfield park today.', datetime(2022, 8, 10, 19, 10, 25), 4, 1, [1, 8], [])
    ]

def test_get_all_peeps_by_user(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.get_all_by_user(4) == [
        Peep(15, 'Kayaking at the lake.', datetime(2023, 5, 30, 17, 59, 4), 56, 4, [1, 4, 8], []),
        Peep(14, 'A picture I painted in Turkey.', datetime(2023, 5, 30, 11, 2, 59), 45330, 4, [3, 4, 7, 8, 11], [1]),
        Peep(6, 'Delicious 4 cheese pizza I made!', datetime(2022, 8, 31, 18, 52, 58), 24, 4, [2, 4, 7], [])
    ]
    assert repo.get_all_by_user(2) == [
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, [4, 11], []),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, [4, 12], []),
        Peep(4, 'Who wants to go for food tonight?', datetime(2022, 8, 11, 15, 22, 33), 5, 2, [2, 9], []),
        Peep(2, 'This ice cream is amazing!', datetime(2022, 8, 10, 19, 25, 6), 7, 2, [2], [])
    ]

def test_get_all_peeps_by_tag(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.get_all_by_tag(11) == [
        Peep(14, 'A picture I painted in Turkey.', datetime(2023, 5, 30, 11, 2, 59), 45330, 4, [3, 4, 7, 8, 11], [1]),
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, [4, 11], [])
    ]
    assert repo.get_all_by_tag(4) == [
        Peep(15, 'Kayaking at the lake.', datetime(2023, 5, 30, 17, 59, 4), 56, 4, [1, 4, 8], []),
        Peep(14, 'A picture I painted in Turkey.', datetime(2023, 5, 30, 11, 2, 59), 45330, 4, [3, 4, 7, 8, 11], [1]),
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, [4, 11], []),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, [4, 12], []),
        Peep(6, 'Delicious 4 cheese pizza I made!', datetime(2022, 8, 31, 18, 52, 58), 24, 4, [2, 4, 7], [])
    ]

def test_find_peep_by_id(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.find_by_id(7) == Peep(7, 'A brilliant book about magic.',
                                    datetime(2022, 8, 31, 19, 30, 29), 8, 2, [4, 12], [])
    assert repo.find_by_id(24) == None

@freeze_time("2023-08-10 12:00:01")
def test_add_peep(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.add_peep("July is the best month of the year!", 4,
                        [1, 8]) == 16
    assert repo.add_peep("There are so many llamas in Chile!", 2,
                        [3, 8]) == ["llama"]
    assert repo.add_peep("Does Piers Morgan read the Daily Mail?", 3,
                        [4]) == ['daily mail', 'morgan']
    assert repo.add_peep("Download Festival is always a blast!", 2,
                        [1, 5, 6, 9]) == 17
    assert repo.find_by_id(16) == Peep(16, "July is the best month of the year!",
                                    datetime(2023, 8, 10, 12, 0, 1), 0, 4, [1, 8], [])
    assert repo.get_all_by_tag(1) == [
        Peep(16, "July is the best month of the year!", datetime(2023, 8, 10, 12, 0, 1), 0, 4, [1, 8], []),
        Peep(17, "Download Festival is always a blast!", datetime(2023, 8, 10, 12, 0, 1), 0, 2, [1, 5, 6, 9], []),
        Peep(15, 'Kayaking at the lake.', datetime(2023, 5, 30, 17, 59, 4), 56, 4, [1, 4, 8], []),
        Peep(9, 'A perfect day for a picnic.', datetime(2022, 9, 28, 14, 15, 24), 0, 3, [1, 2, 8], []),
        Peep(3, "It's a brilliant day for the beach.", datetime(2022, 8, 10, 20, 46, 40), 2, 3, [1], []),
        Peep(1, 'I went to Summerfield park today.', datetime(2022, 8, 10, 19, 10, 25), 4, 1, [1, 8], [])
    ]
    assert repo.get_all_by_user(2) == [
        Peep(17, "Download Festival is always a blast!", datetime(2023, 8, 10, 12, 0, 1), 0, 2, [1, 5, 6, 9], []),
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, [4, 11], []),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, [4, 12], []),
        Peep(4, 'Who wants to go for food tonight?', datetime(2022, 8, 11, 15, 22, 33), 5, 2, [2, 9], []),
        Peep(2, 'This ice cream is amazing!', datetime(2022, 8, 10, 19, 25, 6), 7, 2, [2], [])
    ]

def test_peep_belongs_to_user(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.peep_belongs_to_user(7, 2) == True
    assert repo.peep_belongs_to_user(13, 1) == False

def test_does_user_like_peep(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.does_user_like_peep(1, 5) == False
    assert repo.does_user_like_peep(2, 12) == False
    assert repo.does_user_like_peep(5, 15) == True
    assert repo.does_user_like_peep(4, 8) == True

def test_update_likes(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.does_user_like_peep(1, 5) == False
    assert repo.update_likes(1, 5) == 11
    assert repo.does_user_like_peep(1, 5) == True
    assert repo.does_user_like_peep(2, 12) == False
    assert repo.update_likes(2, 12) == 4
    assert repo.does_user_like_peep(2, 12) == True
    assert repo.does_user_like_peep(5, 15) == True
    assert repo.update_likes(5, 15) == 55
    assert repo.does_user_like_peep(5, 15) == False
    assert repo.does_user_like_peep(4, 8) == True
    assert repo.update_likes(4, 8) == 3
    assert repo.does_user_like_peep(4, 8) == False
    assert repo.get_all() == [
        Peep(15, 'Kayaking at the lake.', datetime(2023, 5, 30, 17, 59, 4), 55, 4, [1, 4, 8], []),
        Peep(14, 'A picture I painted in Turkey.', datetime(2023, 5, 30, 11, 2, 59), 45330, 4, [3, 4, 7, 8, 11], [1]),
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, [4, 11], []),
        Peep(12, 'Party at mine tonight!', datetime(2023, 1, 15, 16, 35, 50), 4, 5, [6, 9], []),
        Peep(11, 'Happy New Year from South Korea!', datetime(2023, 1, 1, 0, 4, 56), 130, 1, [3, 5], []),
        Peep(10, 'Merry Christmas everyone!', datetime(2022, 12, 25, 7, 0, 1), 12, 3, [3], []),
        Peep(9, 'A perfect day for a picnic.', datetime(2022, 9, 28, 14, 15, 24), 0, 3, [1, 2, 8], []),
        Peep(8, 'Italy is a brilliant place to visit!', datetime(2022, 9, 27, 23, 49, 14), 3, 5, [3], []),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, [4, 12], []),
        Peep(6, 'Delicious 4 cheese pizza I made!', datetime(2022, 8, 31, 18, 52, 58), 24, 4, [2, 4, 7], []),
        Peep(5, 'Photos from my holiday in spain.', datetime(2022, 8, 23, 10, 2, 3), 11, 1, [3, 8], []),
        Peep(4, 'Who wants to go for food tonight?', datetime(2022, 8, 11, 15, 22, 33), 5, 2, [2, 9], []),
        Peep(3, "It's a brilliant day for the beach.", datetime(2022, 8, 10, 20, 46, 40), 2, 3, [1], []),
        Peep(2, 'This ice cream is amazing!', datetime(2022, 8, 10, 19, 25, 6), 7, 2, [2], []),
        Peep(1, 'I went to Summerfield park today.', datetime(2022, 8, 10, 19, 10, 25), 4, 1, [1, 8], [])
    ]

def test_delete_peep(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    repo.delete(5)
    repo.delete(6)
    repo.delete(4)
    repo.delete(14)
    assert repo.get_all() == [
        Peep(15, 'Kayaking at the lake.', datetime(2023, 5, 30, 17, 59, 4), 56, 4, [1, 4, 8], []),
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, [4, 11], []),
        Peep(12, 'Party at mine tonight!', datetime(2023, 1, 15, 16, 35, 50), 3, 5, [6, 9], []),
        Peep(11, 'Happy New Year from South Korea!', datetime(2023, 1, 1, 0, 4, 56), 130, 1, [3, 5], []),
        Peep(10, 'Merry Christmas everyone!', datetime(2022, 12, 25, 7, 0, 1), 12, 3, [3], []),
        Peep(9, 'A perfect day for a picnic.', datetime(2022, 9, 28, 14, 15, 24), 0, 3, [1, 2, 8], []),
        Peep(8, 'Italy is a brilliant place to visit!', datetime(2022, 9, 27, 23, 49, 14), 4, 5, [3], []),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, [4, 12], []),
        Peep(3, "It's a brilliant day for the beach.", datetime(2022, 8, 10, 20, 46, 40), 2, 3, [1], []),
        Peep(2, 'This ice cream is amazing!', datetime(2022, 8, 10, 19, 25, 6), 7, 2, [2], []),
        Peep(1, 'I went to Summerfield park today.', datetime(2022, 8, 10, 19, 10, 25), 4, 1, [1, 8], [])
    ]
