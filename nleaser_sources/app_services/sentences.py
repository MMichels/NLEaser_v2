from flask_jwt_extended import get_current_user
from pandas import DataFrame

from nleaser_models.datafile import DataFileModel
from nleaser_models.tasks.datafile import DataFileUploadTaskModel
from nleaser_sources.repositories.sentences import delete_sentences_from_datafile
from nleaser_sources.services.sentences import list_sentences_from_datafile
from nleaser_sources.app_services.tasks.sentences import SentenceSaveTaskService


class SentencesService:
    def __init__(self, datafile: DataFileModel):
        self.user = get_current_user()
        self.datafile = datafile

    def import_sentences_from_df(self, df: DataFrame, datafile_import_task: DataFileUploadTaskModel):
        sentences_import_task_service = SentenceSaveTaskService(self.user)
        sentences_import_task_service.create(df, self.datafile, datafile_import_task)

    def list_sentences_from_datafile(self, skip: int, limit: int):
        return list_sentences_from_datafile(self.datafile, skip, limit)

    def delete_sentences_from_datafile(self):
        return delete_sentences_from_datafile(self.datafile)
