class TagRepository:

    def __init__(self, connection):
        self._connection = connection

    def get_all(self):
        rows = self._connection.execute('SELECT * FROM tags')
        return {row['id']:row['name'] for row in rows}
