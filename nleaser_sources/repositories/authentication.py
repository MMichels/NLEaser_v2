from werkzeug.security import check_password_hash
from nleaser_models.user import UserModel


def authenticate(email, password):
    user = UserModel.objects(email=email).first()
    if user and check_password_hash(user.password, password):
        return user


def get_current_user(identity):
    user = UserModel.objects(email=identity['email']).first()
    return user
