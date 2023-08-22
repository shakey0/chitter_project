```python

class User:

    def __init__(self, id, name, user_name, password, d_o_b, current_mood):
        self.id = id
        self.name = name
        self.user_name = user_name
        self.password = password
        self.d_o_b = d_o_b
        self.current_mood = current_mood

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class UserRepository:

    def __init__(self, connection):
        self._connection = connection

    def get_all(self):
        pass
        # gets all the user_data and returns it in a list of User instances

    def get_all_user_names(self):
        pass
        # gets all the user_data and returns a list of usernames

    def find_by_id(self, id):
        pass
        # returns the user according to the id, or None

    def find_by_user_name(self, user_name):
        pass
        # returns the user according to the username, or None

    def check_valid_password(self, password):
        pass
        # checks the password contains uppercase and lowercase chars, numbers, symbols
        # returns True or a message saying which part or parts failed in sentences
    
    def check_valid_d_o_b(self, d_o_b):
        pass
        # checks the date of birth is a valid date
        # returns True or a message saying the chosen month does not have the chosen day

    def validate_new_user(self, name, user_name, password, confirm_password, d_o_b):
        errors = {}
        # checks the name is valid (not empty)
        # checks the user_name is unique (and not empty)
        # checks the password is valid
        # checks the passwords match
        # checks the d_o_b is valid
        # for any that are invalid, a dictionary item will be added with a message (or list of message(s) in the case of the valid_password)
        # if the dictionary is empty, True will be returned, otherwise, the dictionary will be returned

    def add_user(self, name, user_name, password, confirm_password, d_o_b):
        pass
        # checks if everything is valid
        # adds the users and returns the ID if all is valid, others returns the dictionary

    def user_name_password_match(self, user_name, password):
        pass
        # checks if the username and password match in the same user from the database
        # if the username cannot be found: returns "Username does not exist."
        # if the username is found but the password doesn't match: returns "Incorrect password."
        # if both match, returns the user_id

    def update(self, id, current_mood=None, password=None):
        pass
        # updates a part of the user_data for the user (current_mood or password)

    def delete(self, id, password):
        pass
        # deletes the user, requires the password to match


class Peep:

    def __init__(self, id, content, time, likes, user_id):
        self.id = id
        self.content = content
        self.time = time
        self.likes = likes
        self.user_id = user_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class PeepRepository:

    def __init__(self, connection):
        self._connection = connection

    def get_all(self):
        pass
        # gets all the peep data and returns them in a list sorted in reverse chronological order

    def get_all_by_user(self, user_id):
        pass
        # gets all the peep data for peeps that match the user_id and returns them in chron_order

    def get_all_by_tag(self, tag_name):
        pass
        # gets all the peep data for the peeps that are joined to the tags and returns them in chron_order

    def find_by_id(self, id):
        pass
        # gets all the peep data for the peep that matches the id

    def does_not_contain_bad_words(self, content):
        pass
        # returns True if the peep doesn't contain any bad words
        # returns the bad words in a list if the peep contains bad words
        # ['hornet', 'llama', 'scotch egg', 'thameslink', 'daily mail', 'morgan', 'home office']

    def add_peep(self, content, user_id, tags):
        pass
        # checks the peep for bad words and returns the new peep id if okay or a list of bad words if not okay

    def peep_belongs_to_user(self, peep_id, user_id):  # MAY NOT NEED THIS METHOD !!!!!!!!!!
        pass
        # returns True if peep.user_id matches user_id

    def does_user_like_peep(self, user_id, peep_id):
        pass
        # returns True if the user already likes the peep or False if not
        # (checks in the users_peeps to see if a match exists)

    def update_likes(self, user_id, peep_id, like):
        pass
        # adds or subtracts 1 from the number of likes for the peep and updates the users_peeps table
    
    def delete(self, peep_id):
        pass
        # deletes the peep


class TagRepository:

    def __init__(self, connection):
        self._connection = connection

    def get_all(self):
        pass
        # gets all the tags and returns them

    def does_user_favour_tag(self, user_id, tag_id):
        pass
        # returns True if the user and tag are connected (the user likes this topic)
        # otherwise returns False

    def add_tag_to_user(self, user_id, tag_id):
        pass
        # adds the user_id and tag_id to the users_tags table

    def remove_tag_from_user(self, user_id, tag_id):
        pass
        # removes the user_id and tag_id from the users_tags table

    def add_tag_to_peep(self, peep_id, tag_id):
        pass
        # adds the peep_id and tag_id to the peeps_tags table

    def remove_tag_from_peep(self, peep_id, tag_id):
        pass
        # removes the peep_id and tag_id from the peeps_tags table

    def get_users_tags(self, user_id):
        pass
        # returns all the tags found in the users_tags table for the user_id

    def get_peeps_tags(self, peep_id):
        pass
        # returns all the tags found in the peeps_tags table fro the peep_id
