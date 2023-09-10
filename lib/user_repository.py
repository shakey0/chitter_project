from lib.user import *
import re

class UserRepository:

    def __init__(self, connection):
        self._connection = connection

    def get_all(self):
        rows = self._connection.execute('SELECT * FROM users')
        return sorted([User(row['id'], row['name'], row['user_name'], row['password'], row['d_o_b'],
                    row['current_mood']) for row in rows], key=lambda user: user.id)

    def get_all_user_names(self):
        all_users = self.get_all()
        return [user.user_name for user in all_users]

    def find_by_id(self, id):
        rows = self._connection.execute('SELECT * FROM users WHERE id = %s', [id])
        if len(rows) == 0:
            return None
        row = rows[0]
        return User(row['id'], row['name'], row['user_name'], row['password'], row['d_o_b'],
                    row['current_mood'])

    def find_by_user_name(self, user_name):
        rows = self._connection.execute('SELECT * FROM users WHERE user_name = %s', [user_name])
        if len(rows) == 0:
            return None
        row = rows[0]
        return User(row['id'], row['name'], row['user_name'], row['password'], row['d_o_b'],
                    row['current_mood'])

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
            return validation_messages
    
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
        if " " in user_name:
            errors['user_name'] = 'Username cannot have spaces!'
        if user_name in self.get_all_user_names():
            errors['user_name'] = 'Username taken!'
        password_check = self.check_valid_password(password)
        if password_check != True:
            errors['password'] = password_check
        if password != confirm_password:
            errors['pws_match'] = 'Passwords do not match!'
        d_o_b_check = self.check_valid_d_o_b(d_o_b)
        if d_o_b_check != True:
            errors['date'] = d_o_b_check
        if len(errors) == 0:
            return True
        return errors

    def add_user(self, name, user_name, password, confirm_password, d_o_b):
        validity_check = self.validate_new_user(name, user_name, password, confirm_password, d_o_b)
        if validity_check != True:
            return validity_check
        month_to_number = {"January": 1, "February": 2, "March": 3, "April": 4,
                            "May": 5, "June": 6, "July": 7, "August": 8,
                            "September": 9, "October": 10, "November": 11, "December": 12}
        date = f"{d_o_b[2]}/{month_to_number[d_o_b[1]]}/{d_o_b[0]}"
        rows = self._connection.execute('INSERT INTO users (name, user_name, password, d_o_b, current_mood) VALUES (%s, %s, %s, %s, %s) RETURNING id',
                                        [name, user_name, password, date, 'content'])
        return rows[0]['id']

    def user_name_password_match(self, user_name, password):
        all_users = self.get_all()
        for user in all_users:
            if user.user_name == user_name:
                if user.password == password:
                    return user.id
                else:
                    return "Incorrect password."
        return "Username does not exist."

    def update(self, id, current_mood=None, password=None, confirm_password=None):
        if current_mood != None:
            self._connection.execute('UPDATE users SET current_mood = %s WHERE id = %s',
                                    [current_mood, id])
        if password != None:
            password_check = self.check_valid_password(password)
            if password_check == True:
                if password == confirm_password:
                    self._connection.execute('UPDATE users SET password = %s WHERE id = %s', [password, id])
                else:
                    return 'Passwords do not match!'
            else:
                return password_check

    def delete(self, id, password):
        user = self.find_by_id(id)
        if user.password != password:
            return "Incorrect password."
        self._connection.execute('DELETE FROM users WHERE id = %s', [id])
