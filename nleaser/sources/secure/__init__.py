from cryptography.fernet import Fernet

from nleaser.models.user import UserModel


def load_cipher(user: UserModel):
    """
    carrega o cipher utilizado para CRIPTOGRAFAR com base no certificado RSA do usuario
    Args:
        user: usuario dono das sentenças

    Returns:
        Cipher PUBLICO (CRIPTOGRAFA)
    """
    cipher = Fernet(user.cipher_password)
    return cipher
