class Peep:

    def __init__(self, id, content, time, likes, user_id):
        self.id = id
        self.content = content
        self.time = time
        self.likes = likes
        self.user_id = user_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Peep({self.id}, {self.content}, {self.time}, {self.likes}, {self.user_id})"