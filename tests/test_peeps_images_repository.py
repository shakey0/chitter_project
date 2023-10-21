from ChitterApp.lib.repositories.peeps_images_repository import PeepsImagesRepository

def test_get_all(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepsImagesRepository(db_connection)
    assert repo.get_all() == [{'id':1, 'file_name':'Megeve_SimonGarnier_150119_004.jpg', 'peep_id':14}]

def test_get_image_file_name(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepsImagesRepository(db_connection)
    assert repo.get_image_file_name(1) == 'Megeve_SimonGarnier_150119_004.jpg'
    assert repo.get_image_file_name(4) == None

def test_add_image_for_peep(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepsImagesRepository(db_connection)
    assert repo.add_image_for_peep('Snowy_Desert.jpg', 6) == 2
    assert repo.get_image_file_name(1) == 'Megeve_SimonGarnier_150119_004.jpg'
    assert repo.get_image_file_name(2) == 'Snowy_Desert.jpg'
    assert repo.get_image_file_name(7) == None

def test_delete_image_for_peep(db_connection):
    db_connection.seed('seeds/chitter_data.sql')
    repo = PeepsImagesRepository(db_connection)
    assert repo.delete_image_for_peep(1) == None
    assert repo.get_image_file_name(1) == None
