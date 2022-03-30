from flask_jwt_extended import get_current_user

from nleaser_models.nlp.wordcloud import WordcloudModel
from nleaser_models.tasks.wordcloud import WordcloudCreateTaskModel
from nleaser_sources.app_services.datafile import DataFileAppService
from nleaser_sources.app_services.tasks.wordcloud import WordcloudCreateTaskService
from nleaser_sources.services.cipher import load_cipher
from nleaser_sources.repositories.wordcloud import delete_wordclouds_from_datafile, get_wordclouds_from_datafile


class WordcloudAppService:
    def __init__(self, datafile_id: str = None):
        self.user = get_current_user()
        self.datafile = DataFileAppService().get_datafile(datafile_id)

    def create_wordcloud(self) -> WordcloudCreateTaskModel:
        service = WordcloudCreateTaskService(self.user)
        create_wordcloud_task = service.create(self.datafile)
        return create_wordcloud_task

    def get_wordcloud(self) -> WordcloudModel:
        wcs = get_wordclouds_from_datafile(self.datafile)
        wc: WordcloudModel = wcs.first()
        if wc:
            private_cipher = load_cipher(self.user)
            wc.base64_image = private_cipher.decrypt(wc.base64_image.encode()).decode()
            return wc
        else:
            raise FileNotFoundError("Ooops, nada por aqui ainda....")

    def delete_wordcloud(self) -> bool:
        deleted = delete_wordclouds_from_datafile(self.datafile)
        return deleted
