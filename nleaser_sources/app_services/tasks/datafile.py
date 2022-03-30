from nleaser_models.tasks.datafile import DataFileUploadTaskModel, DataFileUploadTaskSchema
from nleaser_models.user import UserModel
from . import BaseTaskService


class DataFileUploadTaskService(BaseTaskService):
    def __init__(self, user: UserModel):
        super().__init__(user, DataFileUploadTaskModel, "NLEaser.nleaser_worker_sentence_import")
        self.schema = DataFileUploadTaskSchema()

    def create(self, imported_datafile: dict):
        datafile_import_task: DataFileUploadTaskModel = self.schema.load({
            "owner": str(self.user.id),
            "total": imported_datafile["df"].shape[0],
            "datafile": str(imported_datafile["datafile"].id)
        })
        datafile_import_task.save()
        super(DataFileUploadTaskService, self).create(str(datafile_import_task.id))
        return datafile_import_task