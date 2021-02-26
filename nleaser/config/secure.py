import safebox


def crypt(message: str) -> str:
    """
    Criptografa uma string utilizando a dll
    Args:
        message: string paara criptrografar

    Returns: string criptografada
    """
    crypted_bts = safebox.crypt(message.encode())
    return crypted_bts.decode()


def decrypt(cipher: str) -> str:
    """
    Descriptografa uma string utilizaando a dll
    Args:
        cipher: string criptografada

    Returns: string descriptografada
    """
    decrypted_bts = safebox.decrypt(cipher.encode())
    return decrypted_bts.decode()


if __name__ == "__main__":
    mensagem = "teste 123 !@#"
    c = crypt(mensagem)
    d = decrypt(c)

    print(mensagem)
    print(c)
    print(d)