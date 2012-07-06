class User(object):
    def __init__(self, username="admin", email=None):
        self.username = username
        self.email = email

    def save(self):
        return True

