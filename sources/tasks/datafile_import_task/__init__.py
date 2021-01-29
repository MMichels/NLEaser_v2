from models.datafile import DataFileModel
from models.tasks.datafile_import import DataFileImportModel, DataFileImportSchema
from models.user import UserModel

from sources.tasks.sentences_import_task import SentenceImportTaskService


class DataFileImportTaskService:
    def __init__(self, user: UserModel, imported_datafile: dict):
        self.user = user
        self.imported_datafile = imported_datafile
        self.datafile_import_schema = DataFileImportSchema()

    def create(self):
        datafile_import_task: DataFileImportModel = self.datafile_import_schema.load({
            "owner": self.user,
            "total": self.imported_datafile["df"].shape[1],
            "datafile": self.imported_datafile["datafile"]
        })
        datafile_import_task.save()
        return datafile_import_task
