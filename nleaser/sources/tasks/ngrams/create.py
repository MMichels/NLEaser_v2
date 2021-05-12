import json

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
