from flask_jwt_extended import get_current_user

from nleaser.models.tasks.wordcloud.create import WordcloudCreateTaskModel
from nleaser.models.nlp_extracted_data.wordcloud import WordcloudModel
from nleaser.sources.datafile import DataFileService
from nleaser.sources.secure import load_cipher
from nleaser.sources.tasks.wordcloud.create import WordcloudCreateTaskService
from nleaser.sources.wordcloud.services import delete_wordclouds_from_datafile, get_wordclouds_from_datafile


class WordcloudService:
    def __init__(self, datafile_id: str = None):
        self.user = get_current_user()
        self.datafile = DataFileService().get_datafile(datafile_id)

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
            raise FileNotFoundError("Nenhum wordcloud encontrado")

    def delete_wordcloud(self) -> bool:
        deleted = delete_wordclouds_from_datafile(self.datafile)
        return deleted
