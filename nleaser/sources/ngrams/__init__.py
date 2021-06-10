from flask_jwt_extended import get_current_user

from nleaser.models.nlp_extracted_data.ngrams import ExtractedNGramsModel
from nleaser.models.tasks.ngrams.create import NGramsCreateTaskModel
from nleaser.sources.datafile import DataFileService
from nleaser.sources.ngrams.services import get_ngrams_from_datafile, delete_ngrams_from_datafile
from nleaser.sources.tasks.ngrams.create import NGramsCreateTaskService


class NGramsService:
    def __init__(self, datafile_id: str):
        self.user = get_current_user()
        self.datafile = DataFileService().get_datafile(datafile_id)

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
        raise FileNotFoundError("Nenhum NGram encontrado")

    def delete_ngram(self) -> bool:
        deleted = delete_ngrams_from_datafile(self.datafile)
        return deleted


