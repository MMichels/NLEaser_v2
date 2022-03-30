from flask_jwt_extended import get_current_user

from nleaser_models.nlp.ngrams import ExtractedNGramsModel
from nleaser_models.tasks.ngrams import NGramsCreateTaskModel
from nleaser_sources.app_services.datafile import DataFileAppService
from nleaser_sources.app_services.tasks.ngrams import NGramsCreateTaskService
from nleaser_sources.repositories.ngrams import get_ngrams_from_datafile, delete_ngrams_from_datafile


class NGramsAppService:
    def __init__(self, datafile_id: str):
        self.user = get_current_user()
        self.datafile = DataFileAppService().get_datafile(datafile_id)

    def create_ngram(self, size: int) -> NGramsCreateTaskModel:
        service = NGramsCreateTaskService(self.user)
        create_ngram_task = service.create(self.datafile, size)
        return create_ngram_task

    def get_ngram(
            self, skip: int, limit: int, order_by: str = "relevance",
            order_ascending: bool = False) -> ExtractedNGramsModel:
        ngrams = get_ngrams_from_datafile(self.datafile, skip, limit, order_by, bool(order_ascending))
        if ngrams:
            return ngrams
        raise FileNotFoundError("Ooops, nada por aqui ainda....")

    def delete_ngram(self) -> bool:
        deleted = delete_ngrams_from_datafile(self.datafile)
        return deleted


