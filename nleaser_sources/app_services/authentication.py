from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, get_jwt_identity

from nleaser_models.user import UserSchema
from nleaser_sources.repositories.authentication import authenticate, get_current_user


jwt = JWTManager()
jwt.user_loader_callback_loader(get_current_user)


class AuthenticationAppService:
    def __init__(self):
        self.schema = UserSchema()

    def authenticate(self, email, password):
        try:
            user = authenticate(email, password)
            if user:
                access_token = create_access_token(self.schema.dump(user))
                return access_token
        except Exception as e:
            raise e

    def get_current_user(self):
        return get_jwt_identity()
