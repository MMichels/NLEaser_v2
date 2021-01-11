import pandas as pd

from werkzeug.datastructures import FileStorage
from sources.datafile.exceptions import FileReadException, InvalidFormatException


def open_file(file: FileStorage, format: str, sep: str):
    df = None
    if format == 'txt':
        try:
            with open(file) as f:
                sentences = f.readlines()
                df = pd.DataFrame(
                    sentences,
                    columns=['sentences']
                )
        except Exception as e:
            raise FileReadException("Erro ao ler o arquivo", file, e)
    elif format == 'csv':
        try:
            df = pd.read_csv(file, sep=sep)
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


def generate_df_hash(df: pd.DataFrame):
    samples = df.sample(frac=0.5, random_state=42)
    rows_hash = pd.util.hash_pandas_object(samples)
    file_hash = hash(tuple(rows_hash.tolist()))
    return str(file_hash)
