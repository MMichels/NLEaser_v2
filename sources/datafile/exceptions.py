class FileReadException(Exception):
    # Ocorreu um erro ao ler o arquivo, possivelmente por conta do formato incorreto.
    pass


class InvalidFormatException(Exception):
    # O formato informado não possui suporte, ainda.
    pass


class TextColumnNotFound(Exception):
    pass