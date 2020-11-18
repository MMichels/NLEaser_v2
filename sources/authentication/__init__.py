from flask_jwt_extended import JWTManager
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import UserModel

jwt = JWTManager()


def authenticate(email, password):
    user = UserModel.objects(email=email).first()
    if user and check_password_hash(user.password, password):
        return user


