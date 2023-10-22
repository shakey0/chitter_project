from ChitterApp.lib.models.peep import Peep
from datetime import datetime

class PeepRepository:

    def __init__(self, connection):
        self._connection = connection

    def get_tags_for_peep(self, peep_id):
        tags = self._connection.execute('SELECT id FROM tags '
                                        'JOIN peeps_tags ON peeps_tags.tag_id = tags.id '
                                        'WHERE peeps_tags.peep_id = %s', [peep_id])
        return [tag['id'] for tag in tags]
    
    def get_images_for_peep(self, peep_id):
        images = self._connection.execute('SELECT id FROM peeps_images WHERE peep_id = %s',
                                            [peep_id])
        return [image['id'] for image in images]

    def get_all(self):
        rows = self._connection.execute('SELECT * FROM peeps')
        all_peeps = []
        for row in rows:
            tags = self.get_tags_for_peep(row['id'])
            images = self.get_images_for_peep(row['id'])
            peep = Peep(row['id'], row['content'], row['time'], row['likes'],
                        row['user_id'], tags, images)
            all_peeps.append(peep)
        return sorted(all_peeps, key=lambda peep: peep.time, reverse=True)

    def get_all_by_user(self, user_id):
        all_peeps = self.get_all()
        return [peep for peep in all_peeps if peep.user_id == user_id]

    def get_all_by_tag(self, tag_id):
        rows = self._connection.execute('SELECT peeps.id, peeps.content, peeps.time, '
                                        'peeps.likes, peeps.user_id FROM peeps '
                                        'JOIN peeps_tags ON peeps_tags.peep_id = peeps.id '
                                        'JOIN tags ON tags.id = peeps_tags.tag_id '
                                        'WHERE tags.id = %s', [tag_id])
        all_peeps = []
        for row in rows:
            tags = self.get_tags_for_peep(row['id'])
            images = self.get_images_for_peep(row['id'])
            peep = Peep(row['id'], row['content'], row['time'], row['likes'],
                        row['user_id'], tags, images)
            all_peeps.append(peep)
        return sorted(all_peeps, key=lambda peep: peep.time, reverse=True)

    def find_by_id(self, id):
        rows = self._connection.execute('SELECT * FROM peeps WHERE id = %s', [id])
        if len(rows) == 0:
            return None
        row = rows[0]
        tags = self.get_tags_for_peep(row['id'])
        images = self.get_images_for_peep(row['id'])
        return Peep(row['id'], row['content'], row['time'], row['likes'], row['user_id'], tags, images)

    def does_not_contain_bad_words(self, content):
        bad_words = ['hornet', 'llama', 'scotch egg', 'thameslink', 'daily mail', 'morgan', 'home office']
        bad_words_found = []
        for word in bad_words:
            if word in content.lower():
                bad_words_found.append(word)
        if len(bad_words_found) == 0:
            return True
        return bad_words_found

    def add_peep(self, content, user_id, tags):
        no_bad_words = self.does_not_contain_bad_words(content)
        if no_bad_words != True:
            return no_bad_words
        time = datetime.now()
        rows = self._connection.execute('INSERT INTO peeps (content, time, likes, user_id) VALUES '
                                '(%s, %s, %s, %s) RETURNING id', [content, time, 0, user_id])
        peep_id = rows[0]['id']
        for tag_id in tags:
            self._connection.execute('INSERT INTO peeps_tags (peep_id, tag_id) VALUES (%s, %s)',
                                    [peep_id, tag_id])
        return peep_id

    def peep_belongs_to_user(self, peep_id, user_id):
        peep = self.find_by_id(peep_id)
        return peep.user_id == user_id

    def does_user_like_peep(self, user_id, peep_id):
        rows = self._connection.execute('SELECT * FROM users_peeps WHERE user_id = %s AND peep_id = %s',
                                        [user_id, peep_id])
        if len(rows) == 0:
            return False
        return True

    def update_likes(self, user_id, peep_id):
        peep = self.find_by_id(peep_id)
        if self.does_user_like_peep(user_id, peep_id) == False:
            rows = self._connection.execute('UPDATE peeps SET likes = %s WHERE id = %s RETURNING likes',
                                    [peep.likes + 1, peep_id])
            self._connection.execute('INSERT INTO users_peeps (user_id, peep_id) VALUES (%s, %s)',
                                    [user_id, peep_id])
        else:
            rows = self._connection.execute('UPDATE peeps SET likes = %s WHERE id = %s RETURNING likes',
                                    [peep.likes - 1, peep_id])
            self._connection.execute('DELETE FROM users_peeps WHERE user_id = %s AND peep_id = %s',
                                    [user_id, peep_id])
        new_likes = rows[0]['likes']
        return new_likes

    def delete(self, peep_id):
        self._connection.execute('DELETE FROM peeps WHERE id = %s', [peep_id])
