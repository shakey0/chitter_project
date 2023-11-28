from ChitterApp.lib.models.user import *
import re
import bcrypt
import os
from redis import StrictRedis
production = os.environ.get('PRODUCTION', False)
if production:
    redis = StrictRedis(host='localhost', port=6379, db=0)
else:
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    redis = StrictRedis(host='localhost', port=6379, db=0, password=REDIS_PASSWORD)
from flask import current_app
from datetime import datetime


class UserRepository:

    def __init__(self, connection):
        self._connection = connection

    def get(self, id=None, user_name=None, password=False):
        
        query = '''
            SELECT 
                users.id, 
                users.name, 
                users.user_name, 
        '''

        if password:
            query += 'users.password, '

        query += '''
                users.d_o_b, 
                users.current_mood, 
                STRING_AGG(DISTINCT CAST(tags.id AS TEXT), ',') AS tag_ids 
            FROM users 
            LEFT JOIN users_tags ON users.id = users_tags.user_id 
            LEFT JOIN tags ON users_tags.tag_id = tags.id 
        '''

        params = []

        if id:
            query += 'WHERE users.id = %s '
            params.append(id)
        elif user_name:
            query += 'WHERE users.user_name = %s '
            params.append(user_name)

        query += '''
            GROUP BY users.id, users.name, users.user_name, users.d_o_b, users.current_mood 
            ORDER BY users.id;
        '''

        rows = self._connection.execute(query, params)

        if not rows:
            if password:
                return None, None
            return None

        users = []
        for row in rows:
            tags = row['tag_ids'].split(',') if row['tag_ids'] else []
            tags = [int(tag) for tag in tags]

            user = User(row['id'], row['name'], row['user_name'], row['d_o_b'], row['current_mood'], tags)
            users.append(user)
        
        if password:
            return users[0], rows[0]['password']
        return users[0] if (id or user_name) else users

    def get_user_names(self):
        rows = self._connection.execute("SELECT user_name FROM users")
        return [row['user_name'] for row in rows]


    def check_valid_password(self, password):
        validation_messages = []
        if len(password) < 8:
            validation_messages.append('Password must be at least 8 characters.')
        if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            validation_messages.append('Password must contain uppercase and lowercase characters.')
        if not any(char.isdigit() for char in password):
            validation_messages.append('Password must contain at least 1 number.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            validation_messages.append('Password must contain at least 1 symbol.')
        if not validation_messages:
            return True
        else:
            return '<br>'.join(validation_messages)
    
    def check_valid_d_o_b(self, date_list):
        day, month, year = date_list
        month_days = {'January': 31, 'February': 28, 'March': 31, 'April': 30, 'May': 31, 'June': 30,
                    'July': 31, 'August': 31, 'September': 30, 'October': 31, 'November': 30, 'December': 31}
        if month not in month_days:
            return f"Invalid month: {month}"
        max_day = month_days[month]
        if month == 'February':
            if day > 29:
                return "February only has 28 or 29 days!"
            max_day = 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28
            if day > max_day:
                return f"February only had 28 days in {year}!"
        if not (1 <= day <= max_day):
            return f"{month} only has {max_day} days!"
        return True

    def validate_new_user(self, name, user_name, password, confirm_password, d_o_b):
        errors = {}
        name = name.strip()
        if name == "" or name == None:
            errors['name'] = 'Please provide a name!'
        user_name = user_name.strip()
        if user_name == "" or user_name == None:
            errors['user_name'] = 'Please choose a username!'
        symbols = ['-', '_']
        for letter in user_name:
            if not letter.isalpha() and not letter.isnumeric() and letter not in symbols:
                errors['user_name'] = 'Username can only contain letters, numbers, underscores and dashes!'
        if len(user_name) > 20:
            errors['name'] = 'Username cannot be longer than 20 characters!'
        if user_name in self.get_user_names():
            errors['user_name'] = 'Username taken!'
        if password == "" or password == None:
            errors['password'] = 'Please provide a password!'
        else:
            password = password.strip()
            password_check = self.check_valid_password(password)
            if password_check != True:
                errors['password'] = password_check
            else:
                if confirm_password == "" or confirm_password == None:
                    errors['pws_match'] = 'Please confirm your password!'
                elif password != confirm_password:
                    errors['pws_match'] = 'Passwords do not match!'
        d_o_b_check = self.check_valid_d_o_b(d_o_b)
        if d_o_b_check != True:
            errors['date'] = d_o_b_check
        if len(errors) == 0:
            return True
        return errors

    def create(self, name, user_name, password, confirm_password, d_o_b):
        validity_check = self.validate_new_user(name, user_name, password, confirm_password, d_o_b)
        if validity_check != True:
            return validity_check
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        birthdate_str = f"{d_o_b[2]}-{d_o_b[1]}-{d_o_b[0]}"
        birthdate = datetime.strptime(birthdate_str, "%Y-%B-%d").date()
        rows = self._connection.execute('INSERT INTO users (name, user_name, password, d_o_b, current_mood) '
                                        'VALUES (%s, %s, %s, %s, %s) RETURNING id',
                                        [name, user_name, hashed, birthdate, 'content'])
        return User(rows[0]['id'], name, user_name, birthdate, 'content', [])
    

    def check_user_password(self, id, password):
        hashed_pwd = self._connection.execute('SELECT password FROM users WHERE id = %s', [id])[0]['password']
        return bcrypt.checkpw(password.encode('utf-8'), hashed_pwd)

    def user_name_password_match(self, user_name, password):
        user, user_password = self.get(user_name=user_name, password=True)
        if not user:
            return None
        if user.user_name == user_name and bcrypt.checkpw(password.encode('utf-8'), user_password):
            return user
        

    def update(self, id, current_mood=None, current_password=None, new_password=None, confirm_password=None):
        if current_mood != None:
            self._connection.execute('UPDATE users SET current_mood = %s WHERE id = %s', [current_mood, id])
        if new_password != None:
            if not self.check_user_password(id, current_password):
                return "Current password did not match!"
            password_check = self.check_valid_password(new_password)
            if password_check == True:
                if new_password == confirm_password:
                    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    # hashed_hex = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                    # hex_representation = hashed_hex.hex()
                    self._connection.execute('UPDATE users SET password = %s WHERE id = %s', [hashed, id])
                else:
                    return 'New passwords do not match!'
            else:
                return password_check

    def update_tags(self, user_id, tags_to_remove, tags_to_add):
        if tags_to_remove:
            tags_to_remove_data = [(user_id, tag_id) for tag_id in tags_to_remove]
            self._connection.executemany(
                'DELETE FROM users_tags WHERE user_id = %s AND tag_id = %s',
                tags_to_remove_data
            )
        if tags_to_add:
            tags_to_add_data = [(user_id, tag_id) for tag_id in tags_to_add]
            self._connection.executemany(
                'INSERT INTO users_tags (user_id, tag_id) VALUES (%s, %s)',
                tags_to_add_data
            )


    def delete(self, id, stages):
        if not stages:
            return "INVALID"
        for stage, num in zip(stages, range(4)):
            value = redis.get(f"{id}_stage_{num+1}_auth")
            if value == None or value.decode('utf-8') != stage:
                return "INVALID"
            
        images_from_user = self._connection.execute('''
            SELECT peeps_images.file_name 
            FROM peeps_images 
            JOIN peeps ON peeps_images.peep_id = peeps.id 
            JOIN users ON peeps.user_id = users.id 
            WHERE users.id = %s;
        ''', [id])

        self._connection.execute('DELETE FROM users WHERE id = %s', [id])

        if len(images_from_user) > 0:
            for image in images_from_user:
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image["file_name"])
                os.remove(file_path)
