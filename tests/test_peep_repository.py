from ChitterApp.lib.repositories.peep_repository import PeepRepository
from ChitterApp.lib.models.peep import Peep
from datetime import datetime
from freezegun import freeze_time


def test_get_all_peeps(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.get() == [
        Peep(15, 'Kayaking at the lake.', datetime(2023, 5, 30, 17, 59, 4), 56, 4, 'mousey_14', [1, 4, 8], [], False),
        Peep(14, 'A picture I painted in Turkey.', datetime(2023, 5, 30, 11, 2, 59), 45330, 4, 'mousey_14', [11, 3, 4, 7, 8], ["Megeve_SimonGarnier_150119_004_14.jpg"], False),
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, 'sammy1890', [11, 4], [], False),
        Peep(12, 'Party at mine tonight!', datetime(2023, 1, 15, 16, 35, 50), 3, 5, 'rosy_red', [6, 9], [], False),
        Peep(11, 'Happy New Year from South Korea!', datetime(2023, 1, 1, 0, 4, 56), 130, 1, 'jodesnode', [3, 5], [], False),
        Peep(10, 'Merry Christmas everyone!', datetime(2022, 12, 25, 7, 0, 1), 12, 3, 'son_of_john', [3], [], False),
        Peep(9, 'A perfect day for a picnic.', datetime(2022, 9, 28, 14, 15, 24), 0, 3, 'son_of_john', [1, 2, 8], [], False),
        Peep(8, 'Italy is a brilliant place to visit!', datetime(2022, 9, 27, 23, 49, 14), 4, 5, 'rosy_red', [3], [], False),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, 'sammy1890', [12, 4], [], False),
        Peep(6, 'Delicious 4 cheese pizza I made!', datetime(2022, 8, 31, 18, 52, 58), 24, 4, 'mousey_14', [2, 4, 7], [], False),
        Peep(5, 'Photos from my holiday in spain.', datetime(2022, 8, 23, 10, 2, 3), 10, 1, 'jodesnode', [3, 8], [], False),
        Peep(4, 'Who wants to go for food tonight?', datetime(2022, 8, 11, 15, 22, 33), 5, 2, 'sammy1890', [2, 9], [], False),
        Peep(3, "It's a brilliant day for the beach.", datetime(2022, 8, 10, 20, 46, 40), 2, 3, 'son_of_john', [1], [], False),
        Peep(2, 'This ice cream is amazing!', datetime(2022, 8, 10, 19, 25, 6), 7, 2, 'sammy1890', [2], [], False),
        Peep(1, 'I went to Summerfield park today.', datetime(2022, 8, 10, 19, 10, 25), 4, 1, 'jodesnode', [1, 8], [], False)
    ]


def test_get_all_peeps_by_user(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.get(user_id=4) == [
        Peep(15, 'Kayaking at the lake.', datetime(2023, 5, 30, 17, 59, 4), 56, 4, 'mousey_14', [1, 4, 8], [], False),
        Peep(14, 'A picture I painted in Turkey.', datetime(2023, 5, 30, 11, 2, 59), 45330, 4, 'mousey_14', [11, 3, 4, 7, 8], ["Megeve_SimonGarnier_150119_004_14.jpg"], False),
        Peep(6, 'Delicious 4 cheese pizza I made!', datetime(2022, 8, 31, 18, 52, 58), 24, 4, 'mousey_14', [2, 4, 7], [], False)
    ]
    assert repo.get(user_id=2) == [
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, 'sammy1890', [11, 4], [], False),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, 'sammy1890', [12, 4], [], False),
        Peep(4, 'Who wants to go for food tonight?', datetime(2022, 8, 11, 15, 22, 33), 5, 2, 'sammy1890', [2, 9], [], False),
        Peep(2, 'This ice cream is amazing!', datetime(2022, 8, 10, 19, 25, 6), 7, 2, 'sammy1890', [2], [], False)
    ]


def test_get_peep_by_id(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.get(peep_id=7) == Peep(7, 'A brilliant book about magic.',
                                        datetime(2022, 8, 31, 19, 30, 29), 8, 2, 'sammy1890', [12, 4], [], False)
    assert repo.get(peep_id=24) == None


@freeze_time("2023-08-10 12:00:01")
def test_create_peep(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.create("July is the best month of the year!", 4, [1, 8], []) == 16
    assert repo.create("There are so many hornets in Japan!", 2, [3, 8], []) == ["hornet"]
    assert repo.create("Does Piers Morgan read the Daily Mail?", 3, [4], []) == ['daily mail', 'piers morgan']
    assert repo.create("Download Festival is always a blast!", 2, [1, 5, 6, 9], []) == 17
    assert repo.get(peep_id=16) == Peep(16, "July is the best month of the year!",
                                    datetime(2023, 8, 10, 12, 0, 1), 0, 4, 'mousey_14', [1, 8], [], False)
    assert repo.get(user_id=2) == [
        Peep(17, "Download Festival is always a blast!", datetime(2023, 8, 10, 12, 0, 1), 0, 2, 'sammy1890', [1, 5, 6, 9], [], False),
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, 'sammy1890', [11, 4], [], False),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, 'sammy1890', [12, 4], [], False),
        Peep(4, 'Who wants to go for food tonight?', datetime(2022, 8, 11, 15, 22, 33), 5, 2, 'sammy1890', [2, 9], [], False),
        Peep(2, 'This ice cream is amazing!', datetime(2022, 8, 10, 19, 25, 6), 7, 2, 'sammy1890', [2], [], False)
    ]


def test_update_tags(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    repo.update_tags(14, [3, 8], [1, 12])
    repo.update_tags(10, [], [11])
    repo.update_tags(4, [], [3, 10])
    repo.update_tags(1, [8], [])
    repo.update_tags(9, [1, 8], [])
    assert repo.get() == [
        Peep(15, 'Kayaking at the lake.', datetime(2023, 5, 30, 17, 59, 4), 56, 4, 'mousey_14', [1, 4, 8], [], False),
        Peep(14, 'A picture I painted in Turkey.', datetime(2023, 5, 30, 11, 2, 59), 45330, 4, 'mousey_14', [1, 11, 12, 4, 7], ["Megeve_SimonGarnier_150119_004_14.jpg"], False),
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, 'sammy1890', [11, 4], [], False),
        Peep(12, 'Party at mine tonight!', datetime(2023, 1, 15, 16, 35, 50), 3, 5, 'rosy_red', [6, 9], [], False),
        Peep(11, 'Happy New Year from South Korea!', datetime(2023, 1, 1, 0, 4, 56), 130, 1, 'jodesnode', [3, 5], [], False),
        Peep(10, 'Merry Christmas everyone!', datetime(2022, 12, 25, 7, 0, 1), 12, 3, 'son_of_john', [11, 3], [], False),
        Peep(9, 'A perfect day for a picnic.', datetime(2022, 9, 28, 14, 15, 24), 0, 3, 'son_of_john', [2], [], False),
        Peep(8, 'Italy is a brilliant place to visit!', datetime(2022, 9, 27, 23, 49, 14), 4, 5, 'rosy_red', [3], [], False),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, 'sammy1890', [12, 4], [], False),
        Peep(6, 'Delicious 4 cheese pizza I made!', datetime(2022, 8, 31, 18, 52, 58), 24, 4, 'mousey_14', [2, 4, 7], [], False),
        Peep(5, 'Photos from my holiday in spain.', datetime(2022, 8, 23, 10, 2, 3), 10, 1, 'jodesnode', [3, 8], [], False),
        Peep(4, 'Who wants to go for food tonight?', datetime(2022, 8, 11, 15, 22, 33), 5, 2, 'sammy1890', [10, 2, 3, 9], [], False),
        Peep(3, "It's a brilliant day for the beach.", datetime(2022, 8, 10, 20, 46, 40), 2, 3, 'son_of_john', [1], [], False),
        Peep(2, 'This ice cream is amazing!', datetime(2022, 8, 10, 19, 25, 6), 7, 2, 'sammy1890', [2], [], False),
        Peep(1, 'I went to Summerfield park today.', datetime(2022, 8, 10, 19, 10, 25), 4, 1, 'jodesnode', [1], [], False)
    ]


def test_update_likes(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    assert repo.update_likes(1, 5, False) == 11
    assert repo.update_likes(2, 12, False) == 4
    assert repo.update_likes(5, 15, True) == 55
    assert repo.update_likes(4, 8, True) == 3
    assert repo.get() == [
        Peep(15, 'Kayaking at the lake.', datetime(2023, 5, 30, 17, 59, 4), 55, 4, 'mousey_14', [1, 4, 8], [], False),
        Peep(14, 'A picture I painted in Turkey.', datetime(2023, 5, 30, 11, 2, 59), 45330, 4, 'mousey_14', [11, 3, 4, 7, 8], ["Megeve_SimonGarnier_150119_004_14.jpg"], False),
        Peep(13, 'My fantastic lego house!', datetime(2023, 2, 10, 19, 45, 00), 1602, 2, 'sammy1890', [11, 4], [], False),
        Peep(12, 'Party at mine tonight!', datetime(2023, 1, 15, 16, 35, 50), 4, 5, 'rosy_red', [6, 9], [], False),
        Peep(11, 'Happy New Year from South Korea!', datetime(2023, 1, 1, 0, 4, 56), 130, 1, 'jodesnode', [3, 5], [], False),
        Peep(10, 'Merry Christmas everyone!', datetime(2022, 12, 25, 7, 0, 1), 12, 3, 'son_of_john', [3], [], False),
        Peep(9, 'A perfect day for a picnic.', datetime(2022, 9, 28, 14, 15, 24), 0, 3, 'son_of_john', [1, 2, 8], [], False),
        Peep(8, 'Italy is a brilliant place to visit!', datetime(2022, 9, 27, 23, 49, 14), 3, 5, 'rosy_red', [3], [], False),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, 'sammy1890', [12, 4], [], False),
        Peep(6, 'Delicious 4 cheese pizza I made!', datetime(2022, 8, 31, 18, 52, 58), 24, 4, 'mousey_14', [2, 4, 7], [], False),
        Peep(5, 'Photos from my holiday in spain.', datetime(2022, 8, 23, 10, 2, 3), 11, 1, 'jodesnode', [3, 8], [], False),
        Peep(4, 'Who wants to go for food tonight?', datetime(2022, 8, 11, 15, 22, 33), 5, 2, 'sammy1890', [2, 9], [], False),
        Peep(3, "It's a brilliant day for the beach.", datetime(2022, 8, 10, 20, 46, 40), 2, 3, 'son_of_john', [1], [], False),
        Peep(2, 'This ice cream is amazing!', datetime(2022, 8, 10, 19, 25, 6), 7, 2, 'sammy1890', [2], [], False),
        Peep(1, 'I went to Summerfield park today.', datetime(2022, 8, 10, 19, 10, 25), 4, 1, 'jodesnode', [1, 8], [], False)
    ]


def test_delete_peep(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepRepository(db_connection)
    repo.delete(5, [])
    repo.delete(6, [])
    repo.delete(4, [])
    repo.delete(13, [])
    assert repo.get() == [
        Peep(15, 'Kayaking at the lake.', datetime(2023, 5, 30, 17, 59, 4), 56, 4, 'mousey_14', [1, 4, 8], [], False),
        Peep(14, 'A picture I painted in Turkey.', datetime(2023, 5, 30, 11, 2, 59), 45330, 4, 'mousey_14', [11, 3, 4, 7, 8], ["Megeve_SimonGarnier_150119_004_14.jpg"], False),
        Peep(12, 'Party at mine tonight!', datetime(2023, 1, 15, 16, 35, 50), 3, 5, 'rosy_red', [6, 9], [], False),
        Peep(11, 'Happy New Year from South Korea!', datetime(2023, 1, 1, 0, 4, 56), 130, 1, 'jodesnode', [3, 5], [], False),
        Peep(10, 'Merry Christmas everyone!', datetime(2022, 12, 25, 7, 0, 1), 12, 3, 'son_of_john', [3], [], False),
        Peep(9, 'A perfect day for a picnic.', datetime(2022, 9, 28, 14, 15, 24), 0, 3, 'son_of_john', [1, 2, 8], [], False),
        Peep(8, 'Italy is a brilliant place to visit!', datetime(2022, 9, 27, 23, 49, 14), 4, 5, 'rosy_red', [3], [], False),
        Peep(7, 'A brilliant book about magic.', datetime(2022, 8, 31, 19, 30, 29), 8, 2, 'sammy1890', [12, 4], [], False),
        Peep(3, "It's a brilliant day for the beach.", datetime(2022, 8, 10, 20, 46, 40), 2, 3, 'son_of_john', [1], [], False),
        Peep(2, 'This ice cream is amazing!', datetime(2022, 8, 10, 19, 25, 6), 7, 2, 'sammy1890', [2], [], False),
        Peep(1, 'I went to Summerfield park today.', datetime(2022, 8, 10, 19, 10, 25), 4, 1, 'jodesnode', [1, 8], [], False)
    ]
