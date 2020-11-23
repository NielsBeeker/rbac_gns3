"""
This class contains the different things about endpoint required for user verification
"""
class ObjectAcl:
    def __init__(self, action: str, roles: [(str, str)]):
        self.action = action

        self.roles = roles

    def get_role(self):
        return self.roles

    def get_action(self):
        return self.action
