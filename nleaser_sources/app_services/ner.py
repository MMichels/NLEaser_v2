from flask_jwt_extended import get_current_user

from nleaser_models.nlp.ner import NerResumeModel
from nleaser_models.tasks.ner import NerResumeCreateTaskModel
from nleaser_sources.app_services.datafile import DataFileAppService
from nleaser_sources.app_services.tasks.ner import NerResumeCreateTaskService
from nleaser_sources.repositories.ner import get_ner_resume_from_datafile, delete_ner_resume_from_datafile


class NerResumeAppService:
    def __init__(self, datafile_id: str):
        self.user = get_current_user()
        self.datafile = DataFileAppService().get_datafile(datafile_id)

    def create_ner_resume(self) -> NerResumeCreateTaskModel:
        service = NerResumeCreateTaskService(self.user)
        create_ner_resume_task = service.create(self.datafile)
        return create_ner_resume_task

    def get_ner_resume(
            self, skip: int, limit: int, order_by: str = "count",
            order_ascending: bool = False) -> NerResumeModel:
        ner_resume = get_ner_resume_from_datafile(
            self.datafile, skip, limit, order_by, order_ascending
        )
        if ner_resume:
            return ner_resume
        raise FileNotFoundError("Ooops, nada por aqui ainda....")

    def delete_ner_resume(self) -> bool:
        deleted = delete_ner_resume_from_datafile(self.datafile)
        return deleted
