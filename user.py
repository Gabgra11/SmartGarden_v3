class User:
    def __init__(self, id):
        if not id == None: # ID Passed in:
            self.id = id
            self.is_authenticated = True # We don't create user objects for non-authenticated users
            self.is_active = True # Inactivity not tracked
            self.is_anonymous = False # All users are not anonymous
        else: # id == None:
            self.id = None
            self.is_authenticated = False
            self.is_active = False
            self.is_anonymous = True

    def get_id(self):
        return self.id