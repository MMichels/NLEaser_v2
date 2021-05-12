from flask_jwt_extended import get_current_user

from nleaser.models.tasks.ngrams.create import NGramsCreateTaskSchema
from nleaser.sources.datafile import DataFileService
from nleaser.sources.tasks.ngrams.create import NGramsCreateTaskService


class NGramsService:
    def __init__(self, datafile_id: str):
        self.user = get_current_user()
        self.datafile = DataFileService().get_datafile(datafile_id)

    def create_ngram(self, size: int) -> NGramsCreateTaskSchema:
        service = NGramsCreateTaskService(self.user)
        create_ngram_task = service.create(self.datafile, size)
        return create_ngram_task
