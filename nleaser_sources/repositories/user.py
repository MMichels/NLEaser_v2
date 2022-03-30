from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash
from nleaser_models.user import UserModel


def create_new_user(email, name, password):

    new_user = UserModel(
        email=email,
        name=name,
        password=generate_password_hash(password),
        cipher_password=Fernet.generate_key()
    )
    new_user.save()
    return new_user
