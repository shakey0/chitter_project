from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, name, user_name, d_o_b, current_mood, tags):
        self.id = id
        self.name = name
        self.user_name = user_name
        self.d_o_b = d_o_b
        self.current_mood = current_mood
        self.tags = tags

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"User({self.id}, {self.name}, {self.user_name}, {self.d_o_b}, {self.current_mood}, {self.tags})"
