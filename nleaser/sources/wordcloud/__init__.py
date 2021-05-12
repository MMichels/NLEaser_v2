from flask_jwt_extended import get_current_user

from nleaser.models.datafile import DataFileModel
from nleaser.models.tasks.wordcloud.create import WordcloudCreateTaskModel
from nleaser.models.wordcloud import WordcloudModel
from nleaser.sources.wordcloud.services import delete_wordclouds_from_datafile, get_wordclouds_from_datafile
from nleaser.sources.tasks.wordcloud.create import WordcloudCreateTaskService
from nleaser.sources.secure import load_cipher


class WordcloudService:
    def __init__(self, datafile_id: str = None):
        self.user = get_current_user()

        if datafile_id:
            self.datafile = DataFileModel.objects(
                owner=self.user, id=datafile_id
            ).first()

    def create_wordcloud(self) -> WordcloudCreateTaskModel:
        service = WordcloudCreateTaskService(self.user)
        create_wordcloud_task = service.create(self.datafile)
        return create_wordcloud_task

    def get_wordcloud(self) -> WordcloudModel:
        private_cipher = load_cipher(self.user)
        wcs = get_wordclouds_from_datafile(self.datafile)
        wc: WordcloudModel = wcs.first()
        if wc:
            wc.base64_image = private_cipher.decrypt(wc.base64_image.encode()).decode()
            return wc
        else:
            raise FileNotFoundError("Ainda não existe nenhum wordcloud para esse conjunto de dados")

    def delete_wordcloud(self) -> bool:
        deleted = delete_wordclouds_from_datafile(self.datafile)
        return deleted
