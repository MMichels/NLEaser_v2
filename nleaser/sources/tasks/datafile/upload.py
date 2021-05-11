from datetime import datetime
from mongoengine import QuerySet

from nleaser.models.tasks.datafile.upload import DataFileUploadTaskModel, DataFileUploadTaskSchema
from nleaser.models.user import UserModel


class DataFileUploadTaskService:
    def __init__(self, user: UserModel):
        self.user = user
        self.datafile_import_schema = DataFileUploadTaskSchema()

    def create(self, imported_datafile: dict):
        datafile_import_task: DataFileUploadTaskModel = self.datafile_import_schema.load({
            "owner": str(self.user.id),
            "total": imported_datafile["df"].shape[0],
            "datafile": str(imported_datafile["datafile"].id)
        })
        datafile_import_task.save()
        return datafile_import_task

    def list_current_tasks(self, datafile_id) -> QuerySet:
        tasks = DataFileUploadTaskModel.objects(
            owner=self.user, datafile=datafile_id
        ).order_by("-created_at").limit(5)

        if tasks.count() == 0:
            raise FileNotFoundError("Não existe nenhum tarefa em progresso")

        return tasks

    def list_failed_tasks(self, datafile_id: str, dataInicial: datetime) -> QuerySet:
        failed_Tasks = DataFileUploadTaskModel.objects(
            owner=self.user, datafile=datafile_id,
            created_at__gte=dataInicial, status="error"
        ).order_by("-created_at")

        return failed_Tasks