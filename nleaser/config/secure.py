import os
import sys
import pathlib
import ctypes

directory = pathlib.Path(__file__).parent.absolute().joinpath("resources")
filename = "cripto_debug" if os.getenv("ENV", None).lower().startswith("dev") else "cripto"

if sys.platform == "win32":
    lib = ctypes.WinDLL(str(directory.joinpath(filename+".dll")))
else:
    lib = ctypes.cdll.LoadLibrary(str(directory.joinpath(filename+".so")))

lib.crypt.argtypes = lib.decrypt.argtypes = ctypes.c_char_p,
lib.crypt.restype = lib.decrypt.restype = ctypes.c_char_p


def crypt(message: str) -> str:
    """
    Criptografa uma string utilizando a dll
    Args:
        message: string paara criptrografar

    Returns: string criptografada

    """
    crypted_bts = lib.crypt(message.encode())
    return crypted_bts.decode()


def decrypt(cipher: str) -> str:
    """
    Descriptografa uma string utilizaando a dll
    Args:
        cipher: string criptografada

    Returns: string descriptografada

    """
    decrypted_bts = lib.decrypt(cipher.encode())
    return decrypted_bts.decode()


if __name__ == "__main__":
    mensagem = "teste 123 !@#"
    c = crypt(mensagem)
    d = decrypt(c)

    print(mensagem)
    print(c)
    print(d)