import json
from datetime import datetime

from mongoengine import QuerySet

from nleaser.models.datafile import DataFileModel
from nleaser.models.tasks.ngrams.create import NGramsCreateTaskSchema, NGramsCreateTaskModel
from nleaser.models.user import UserModel

from nleaser.sources.rabbit.producer import RabbitProducer


class NGramsCreateTaskService:
    def __init__(self, user: UserModel):
        self.user = user
        self.schema = NGramsCreateTaskSchema()
        self.producer = RabbitProducer("NLEaser.ngrams_create")

    def create(self, datafile: DataFileModel, size: int) -> NGramsCreateTaskModel:
        model: NGramsCreateTaskModel = self.schema.load({
            "owner": self.user,
            "datafile": datafile,
            "size": size
        })
        model.save()
        self.producer.send_message(
            json.dumps({
                "task": str(model.id)
            })
        )
        return model

    def list_current_tasks(self, datafile_id: str) -> QuerySet:
        tasks = NGramsCreateTaskModel.objects(
            owner=self.user, datafile=datafile_id
        ).order_by("-created_at").limit(5)

        if tasks.count() == 0:
            raise FileNotFoundError("Não existe nenhuma tarefa em progresso")
        return tasks

    def list_failed_tasks(self, datafile_id: str, data_inicial: datetime):
        failed_tasks = NGramsCreateTaskModel.objects(
            owner=self.user, datafile=datafile_id,
            created_at__gte=data_inicial, status="error"
        ).order_by("-created_at")

        return failed_tasks
