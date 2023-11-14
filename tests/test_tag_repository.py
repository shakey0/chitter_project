from ChitterApp.lib.repositories.tag_repository import TagRepository

def test_get_all_tags(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = TagRepository(db_connection)
    assert repo.get_all() == {1: '#DaysOut', 2: '#Food', 3: '#Travel', 4: '#Hobbies',
                            5: '#Festivals', 6: '#Music', 7: '#Art', 8: '#Nature',
                            9: '#Social', 10: '#Work', 11: '#Creative', 12: '#Books'}
