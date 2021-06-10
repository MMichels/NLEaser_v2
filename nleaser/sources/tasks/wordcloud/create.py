from nleaser.models.datafile import DataFileModel
from nleaser.models.tasks.wordcloud.create import WordcloudCreateTaskModel, WordcloudCreateTaskSchema
from nleaser.models.user import UserModel
from nleaser.sources.tasks import BaseTaskService


class WordcloudCreateTaskService(BaseTaskService):
    def __init__(self, user: UserModel):
        super().__init__(user, WordcloudCreateTaskModel, "NLEaser.wordcloud_create")
        self.schema = WordcloudCreateTaskSchema()

    def create(self, datafile: DataFileModel) -> WordcloudCreateTaskModel:
        model: WordcloudCreateTaskModel = self.schema.load({
            "owner": self.user,
            "datafile": datafile,
        })
        model.save()
        super().create(str(model.id))
        return model
