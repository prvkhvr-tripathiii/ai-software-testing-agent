class UserService:

    def __init__(self):
        self.users = []

    def add_user(self, name):
        if not name:
            raise ValueError("Name cannot be empty")

        self.users.append(name)

    def find_user(self, name):
        for user in self.users:
            if user == name:
                return user

        return None

    def risky_operation(self, value):
        try:
            return 100 / value
        except ZeroDivisionError:
            return None