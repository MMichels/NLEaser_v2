from typing import List

from flask_jwt_extended import get_current_user

from nleaser_models.datafile import DataFileModel


from nleaser_sources.app_services.sentences import SentencesService
from nleaser_sources.app_services.tasks.datafile import DataFileUploadTaskService
from nleaser_sources.services.datafile import import_data_file
from nleaser_sources.repositories.datafile import delete_data_file, get_datafile, list_all_user_datafiles


class DataFileAppService:
    def __init__(self):
        self.user = get_current_user()

    def import_datafile(self, file, format: str, text_column: str, language: str, separador=";") -> DataFileModel:
        imported_datafile = import_data_file(self.user, file, format, text_column,
                                             language, separador)

        datafile_import_task_service = DataFileUploadTaskService(
            self.user
        )
        datafile_import_task = datafile_import_task_service.create(imported_datafile)

        sentence_service = SentencesService(imported_datafile["datafile"])

        sentence_service.import_sentences_from_df(
            imported_datafile["df"],
            datafile_import_task
        )

        return imported_datafile["datafile"]

    def list_all_datafiles(self, orderby: str = "name", order_ascending: bool = True) -> List[DataFileModel]:
        documents = list_all_user_datafiles(self.user, orderby, order_ascending)
        return documents

    def get_datafile(self, datafile_id: str) -> DataFileModel:
        return get_datafile(self.user, datafile_id)

    def delete_datafile(self, datafile_id: str) -> bool:
        deleted = delete_data_file(self.user, datafile_id)
        return deleted

    def get_sentences(self, datafile_id: str, skip: int, limit: int):
        datafile = self.get_datafile(datafile_id)
        sentences_service = SentencesService(datafile)
        return sentences_service.list_sentences_from_datafile(skip, limit)
