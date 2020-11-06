class ObjectAcl:
    def __init__(self, action: str, scopes: str , roles: [(str, str)]):
        self.action = action
        self.scopes = scopes
        self.roles = roles

    def get_role(self):
        return self.roles

    def get_action(self):
        return self.action

    def get_scopes(self):
        return self.scopes