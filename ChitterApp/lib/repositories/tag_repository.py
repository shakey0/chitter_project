class TagRepository:

    def __init__(self, connection):
        self._connection = connection

    def get_all(self):
        rows = self._connection.execute('SELECT * FROM tags')
        return {row['id']:row['name'] for row in rows}
    
    def does_user_favour_tag(self, user_id, tag_id):
        rows = self._connection.execute('SELECT * FROM users_tags WHERE user_id = %s AND tag_id = %s',
                                        [user_id, tag_id])
        if len(rows) == 0:
            return False
        return True

    def add_tag_to_user(self, user_id, tag_id):
        if self.does_user_favour_tag(user_id, tag_id) == True:
            return "Already connected!"
        self._connection.execute('INSERT INTO users_tags (user_id, tag_id) VALUES (%s, %s)',
                                    [user_id, tag_id])

    def remove_tag_from_user(self, user_id, tag_id):
        if self.does_user_favour_tag(user_id, tag_id) == False:
            return "Was not connected in the first place!"
        self._connection.execute('DELETE FROM users_tags WHERE user_id = %s AND tag_id = %s',
                                    [user_id, tag_id])

    def tag_is_connected_to_peep(self, peep_id, tag_id):
        rows = self._connection.execute('SELECT * FROM peeps_tags WHERE peep_id = %s AND tag_id = %s',
                                        [peep_id, tag_id])
        if len(rows) == 0:
            return False
        return True

    def add_tag_to_peep(self, peep_id, tag_id):
        if self.tag_is_connected_to_peep(peep_id, tag_id) == True:
            return "Already connected!"
        self._connection.execute('INSERT INTO peeps_tags (peep_id, tag_id) VALUES (%s, %s)',
                                    [peep_id, tag_id])

    def remove_tag_from_peep(self, peep_id, tag_id):
        if self.tag_is_connected_to_peep(peep_id, tag_id) == False:
            return "Was not connected in the first place!"
        self._connection.execute('DELETE FROM peeps_tags WHERE peep_id = %s AND tag_id = %s',
                                    [peep_id, tag_id])

    def get_users_tags(self, user_id):
        rows = self._connection.execute('SELECT * FROM tags '
                                        'JOIN users_tags ON users_tags.tag_id = tags.id '
                                        'WHERE user_id = %s', [user_id])
        return {row['id']:row['name'] for row in rows}

    def get_peeps_tags(self, peep_id):
        rows = self._connection.execute('SELECT * FROM tags '
                                        'JOIN peeps_tags ON peeps_tags.tag_id = tags.id '
                                        'WHERE peep_id = %s', [peep_id])
        return {row['id']:row['name'] for row in rows}
