import json

from mongoengine import QuerySet

from nleaser.models.tasks.wordcloud.create import WordcloudCreateTaskModel, WordcloudCreateTaskSchema
from nleaser.sources.rabbit.producer import RabbitProducer

from nleaser.models.datafile import DataFileModel
from nleaser.models.user import UserModel
from nleaser.sources.logger import create_logger

logger = create_logger(__file__)


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
        return tasks
