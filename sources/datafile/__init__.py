import pandas as pd
from flask_jwt_extended import get_current_user

from werkzeug.datastructures import FileStorage

from models.datafile import DataFileSchema, DataFileModel
from sources.datafile.util import generate_df_hash, open_file
from sources.datafile.exceptions import TextColumnNotFound


def import_data_file(file: FileStorage, format: str, text_column: str, language: str,
                     overwrite: bool = False, separador=";") -> DataFileModel:
    schema = DataFileSchema()
    df = open_file(file, format, separador)

    if format != 'txt':
        if not text_column in df.columns:
            raise TextColumnNotFound("Não foi possivel encontrar a coluna " + text_column + " no conjunto de dados")

    hash = generate_df_hash(df)

    data_file: DataFileModel = schema.load(
        {
            'hash': hash,
            'name': file.filename,
            'format': format,
            'language': language,
            'text_column': text_column
        }
    )
    data_file.owner = get_current_user()
    if overwrite:
        DataFileModel.objects(hash=hash).update_one(
            set__name=data_file.name,
            set__format=data_file.format,
            set__language=data_file.language,
            set__text_column=data_file.text_column,
            upsert=True
        )
    else:
        data_file.save()
    return data_file
