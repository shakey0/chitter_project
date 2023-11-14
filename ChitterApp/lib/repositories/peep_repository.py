from ChitterApp.lib.models.peep import Peep
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import current_app

class PeepRepository:

    def __init__(self, connection):
        self._connection = connection


    def get(self, user_id=None, peep_id=None, current_user_id=None):

        # Select query
        query = '''
            SELECT 
                peeps.id, 
                peeps.content, 
                peeps.time, 
                peeps.likes, 
                peeps.user_id, 
                users.user_name, 
                STRING_AGG(DISTINCT CAST(tags.id AS TEXT), ',') AS tag_ids, 
                STRING_AGG(DISTINCT CAST(peeps_images.file_name AS TEXT), ',') AS image_filenames
        '''

        # Adding the user_likes part if the user is authenticated
        if current_user_id is not None:
            query += '''
                , CASE 
                    WHEN EXISTS (
                        SELECT 1 FROM users_peeps 
                        WHERE user_id = %s AND peep_id = peeps.id
                    ) THEN TRUE 
                    ELSE FALSE 
                END AS user_likes
            '''

        # Join part of the query
        query += '''
            FROM peeps 
            JOIN users ON peeps.user_id = users.id 
            LEFT JOIN peeps_tags ON peeps.id = peeps_tags.peep_id 
            LEFT JOIN tags ON peeps_tags.tag_id = tags.id 
            LEFT JOIN peeps_images ON peeps.id = peeps_images.peep_id
        '''

        params = []
        
        if current_user_id is not None:
            params.append(current_user_id)

        if user_id:
            query += 'WHERE peeps.user_id = %s '
            params.append(user_id)
        elif peep_id:
            query += 'WHERE peeps.id = %s '
            params.append(peep_id)

        # Adding the GROUP BY and ORDER BY parts
        query += '''
            GROUP BY peeps.id, users.user_name, peeps.content, peeps.time, peeps.likes, peeps.user_id 
            ORDER BY peeps.time DESC;
        '''

        # Excute the query and sort the data
        rows = self._connection.execute(query, params)

        all_peeps = []
        for row in rows:
            tags = row['tag_ids'].split(',') if row['tag_ids'] else []
            tags = [int(tag) for tag in tags]
            images = row['image_filenames'].split(',') if row['image_filenames'] else []

            user_likes = row.get('user_likes', False)

            peep = Peep(row['id'], row['content'], row['time'], row['likes'],
                        row['user_id'], row['user_name'], tags, images, user_likes)
            all_peeps.append(peep)

        return all_peeps[0] if peep_id else all_peeps


    def does_not_contain_bad_words(self, content):
        bad_words = ['daily mail', 'trump', 'scotch egg', 'thameslink', 'clarkson', 'piers morgan',
                    'home office', 'thatcher', 'tony abbott', 'hornet', 'churchill']
        bad_words_found = []
        for word in bad_words:
            if word in content.lower():
                bad_words_found.append(word)
        if len(bad_words_found) == 0:
            return True
        return bad_words_found

    def create(self, content, user_id, tags, uploaded_images):
        no_bad_words = self.does_not_contain_bad_words(content)
        if no_bad_words != True:
            return no_bad_words
        time = datetime.now()
        rows = self._connection.execute('INSERT INTO peeps (content, time, likes, user_id) VALUES '
                                '(%s, %s, %s, %s) RETURNING id', [content, time, 0, user_id])
        peep_id = rows[0]['id']

        tags_data = [(peep_id, tag_id) for tag_id in tags]
        self._connection.executemany('INSERT INTO peeps_tags (peep_id, tag_id) VALUES (%s, %s)', tags_data)

        images_data = []
        for file in uploaded_images:
            filename, file_extension = os.path.splitext(file.filename)
            new_filename = f"{filename}_{peep_id}{file_extension}"
            secure_new_filename = secure_filename(new_filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_new_filename)
            file.save(file_path)
            images_data.append((secure_new_filename, peep_id))
        self._connection.executemany('INSERT INTO peeps_images (file_name, peep_id) VALUES (%s, %s)', images_data)
        return peep_id


    def update_tags(self, peep_id, tags_to_remove, tags_to_add):
        if tags_to_remove:
            tags_to_remove_data = [(peep_id, tag_id) for tag_id in tags_to_remove]
            self._connection.executemany(
                'DELETE FROM peeps_tags WHERE peep_id = %s AND tag_id = %s',
                tags_to_remove_data
            )
        if tags_to_add:
            tags_to_add_data = [(peep_id, tag_id) for tag_id in tags_to_add]
            self._connection.executemany(
                'INSERT INTO peeps_tags (peep_id, tag_id) VALUES (%s, %s)',
                tags_to_add_data
            )

    def update_likes(self, user_id, peep_id, liked):

        if liked:
            updated_likes = self._connection.execute(
                'UPDATE peeps SET likes = likes - 1 WHERE id = %s RETURNING likes',
                [peep_id])
            self._connection.execute(
                'DELETE FROM users_peeps WHERE user_id = %s AND peep_id = %s',
                [user_id, peep_id])
            
        else:
            updated_likes = self._connection.execute(
                'UPDATE peeps SET likes = likes + 1 WHERE id = %s RETURNING likes',
                [peep_id])
            self._connection.execute(
                'INSERT INTO users_peeps (user_id, peep_id) VALUES (%s, %s)',
                [user_id, peep_id])

        return updated_likes[0]['likes']


    def delete(self, peep_id, peep_images):
        self._connection.execute('DELETE FROM peeps WHERE id = %s', [peep_id])
        if len(peep_images) > 0:
            for image in peep_images:
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image)
                os.remove(file_path)
