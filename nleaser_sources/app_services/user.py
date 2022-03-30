from nleaser_sources.repositories.user import create_new_user


class UserAppService:
    def __init__(self):
        pass

    def create_new_user(self, email, name, password):
        create_new_user(email, name, password)
