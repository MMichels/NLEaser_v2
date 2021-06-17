import pandas as pd

from werkzeug.datastructures import FileStorage
from nleaser.sources.datafile.exceptions import FileReadException, InvalidFormatException


def open_file(file: FileStorage, format: str, sep: str):
    df = None
    if format == 'txt':
        try:

            with file.stream as fs:
                sentences = fs.readlines()
                decoded_sentences = map(lambda x: x.decode("utf-8"), sentences)
                df = pd.DataFrame(
                    decoded_sentences,
                    columns=['sentences']
                )
        except Exception as e:
            raise FileReadException("Erro ao ler o arquivo", file, e)
    elif format == 'csv':
        try:
            df = pd.read_csv(file, sep=sep)
        except UnicodeDecodeError as ude:
            raise FileReadException("O arquivo precisa estar codificado em UTF-8", file, ude)
        except Exception as e:
            raise FileReadException("Erro ao ler o arquivo", file, e)
    elif format == 'xlsx':
        try:
            df = pd.read_excel(file, engine="openpyxl")
        except Exception as e:
            raise FileReadException("Erro ao ler o arquivo", file, e)

    if df is None:
        raise InvalidFormatException("Não é possivel ler o formato " + format)
    return df

