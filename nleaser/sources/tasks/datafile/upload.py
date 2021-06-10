from nleaser.models.tasks.datafile.upload import DataFileUploadTaskModel, DataFileUploadTaskSchema
from nleaser.models.user import UserModel
from nleaser.sources.tasks import BaseTaskService


class DataFileUploadTaskService(BaseTaskService):
    def __init__(self, user: UserModel):
        super().__init__(user, DataFileUploadTaskModel, "NLEaser.sentence_import")
        self.schema = DataFileUploadTaskSchema()

    def create(self, imported_datafile: dict):
        datafile_import_task: DataFileUploadTaskModel = self.schema.load({
            "owner": str(self.user.id),
            "total": imported_datafile["df"].shape[0],
            "datafile": str(imported_datafile["datafile"].id)
        })
        datafile_import_task.save()
        return datafile_import_task