from typing import List

from nleaser_models.datafile import DataFileSchema, DataFileModel
from nleaser_models.user import UserModel

datafile_schema = DataFileSchema()


def save(filename: str, format: str, language:str, text_column: str, user: UserModel) -> DataFileModel:
    data_file: DataFileModel = datafile_schema.load(
        {
            'name': filename,
            'format': format,
            'language': language,
            'text_column': text_column
        }
    )
    data_file.owner = user
    data_file.save()
    return data_file


def list_all_user_datafiles(user: UserModel, orderby: str = "name", order_ascending: bool = True) -> List[DataFileModel]:
    documents = DataFileModel.objects(
        owner=user
    ).order_by(
        ("+" if order_ascending else "-") + orderby
    ).all()
    return documents


def get_datafile(user: UserModel, datafile_id: str) -> DataFileModel:
    datafile: DataFileModel = DataFileModel.objects(id=datafile_id, owner=user).first()
    if datafile is None:
        raise FileNotFoundError("Não foi encontrado nenhum arquivo com o id informado")
    return datafile


def delete_data_file(user: UserModel, datafile_id: str):
    excluded = DataFileModel.objects(id=datafile_id, owner=user).delete()

    return excluded > 0
