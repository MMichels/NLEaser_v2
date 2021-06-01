import json
from datetime import datetime
from mongoengine import QuerySet

from nleaser.models.tasks.wordcloud.create import WordcloudCreateTaskModel, WordcloudCreateTaskSchema
from nleaser.sources.rabbit.producer import RabbitProducer

from nleaser.models.datafile import DataFileModel
from nleaser.models.user import UserModel


class WordcloudCreateTaskService:
    def __init__(self, user: UserModel):
        self.user = user
        self.schema = WordcloudCreateTaskSchema()
        self.producer = RabbitProducer("NLEaser.wordcloud_create")

    def create(self, datafile: DataFileModel) -> WordcloudCreateTaskModel:
        model: WordcloudCreateTaskModel = self.schema.load({
            "owner": self.user,
            "datafile": datafile,
        })
        model.save()
        self.producer.send_message(json.dumps({
            "task": str(model.id)
        }))
        return model

    def list_current_tasks(self, datafile_id: str) -> QuerySet:
        tasks = WordcloudCreateTaskModel.objects(
            owner=self.user, datafile=datafile_id
        ).order_by("-created_at").limit(5)

        if tasks.count() == 0:
            raise FileNotFoundError("Não existe nenhuma tarefa em progresso")

        return tasks

    def list_failed_tasks(self, datafile_id: str, data_inicial: datetime):
        failed_tasks = WordcloudCreateTaskModel.objects(
            owner=self.user, datafile=datafile_id,
            created_at__gte=data_inicial, status="error"
        ).order_by("-created_at")

        return failed_tasks
