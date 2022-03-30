from werkzeug.datastructures import FileStorage

from nleaser_models.datafile import DataFileModel
from nleaser_models.user import UserModel
from nleaser_sources.repositories.datafile import save
from .exceptions import TextColumnNotFound
from .util import open_file


def import_data_file(
        user: UserModel, file: FileStorage, format: str,
        text_column: str, language: str, separador=";") -> DataFileModel:

    df = open_file(file, format, separador)

    if format != 'txt':
        if not text_column in df.columns:
            raise TextColumnNotFound("Não foi possivel encontrar a coluna " + text_column + " no conjunto de dados")
    else:
        text_column = df.columns[0]

    data_file = save(file.filename, format, language, text_column, user)

    return {
        "df": df,
        "datafile": data_file
    }
