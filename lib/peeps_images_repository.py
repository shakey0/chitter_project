class PeepsImagesRepository:

    def __init__(self, connection):
        self._connection = connection

    def get_all(self):
        rows = self._connection.execute('SELECT * FROM peeps_images')
        return [{'id':row['id'], 'file_name':row['file_name'], 'peep_id':row['peep_id']} for row in rows]

    def get_image_file_name(self, id):
        rows = self._connection.execute('SELECT file_name FROM peeps_images WHERE id = %s', 
                                        [id])
        if len(rows) == 0:
            return None
        return rows[0]['file_name']
    
    def add_image_for_peep(self, file_name, peep_id):
        rows = self._connection.execute('INSERT INTO peeps_images (file_name, peep_id) VALUES '
                                        '(%s, %s) RETURNING id', [file_name, peep_id])
        return rows[0]['id']
    
    def delete_image_for_peep(self, id):
        self._connection.execute('DELETE FROM peeps_images WHERE id = %s', [id])
