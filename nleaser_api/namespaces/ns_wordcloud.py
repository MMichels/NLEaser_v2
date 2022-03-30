from flask_jwt_extended import jwt_required, get_current_user
from flask_restplus import Namespace, Resource, fields

from nleaser_api.error_handler import error_handler
from nleaser_api.request_models import tasks_model, get_tasks_response_model
from nleaser_api.request_models.wordcloud_models import get_response_model, \
    delete_response_model, post_response_model

from nleaser_models.nlp.wordcloud import WordcloudSchema
from nleaser_models.tasks.wordcloud import WordcloudCreateTaskSchema

from nleaser_sources.app_services.wordcloud import WordcloudAppService
from nleaser_sources.app_services.tasks.wordcloud import WordcloudCreateTaskService

from nleaser_sources.logger import create_logger

logger = create_logger(__name__)

ns_wordcloud = Namespace(
    "Wordcloud",
    "Namespace para criar, visualizar e excluir wordclouds"
)

# POST
create_wordcloud_response_model = ns_wordcloud.model(
    "create_wordcloud_response_model", post_response_model
)

# GET
get_wordclouds_response_model = ns_wordcloud.model("get_wordcloud_response_model", get_response_model)

# DELETE
delete_wordcloud_response_model = ns_wordcloud.model("delete_wordcloud_response_model", delete_response_model)

# TASKS
get_wc_tasks_response_model = get_tasks_response_model.copy()
get_wc_tasks_response_model["tasks"] = fields.Nested(
    ns_wordcloud.model("wc_tasks_model", tasks_model),
    as_list=True
)
get_wc_tasks_response_model = ns_wordcloud.model("get_wc_tasks_response_model", get_wc_tasks_response_model)


@ns_wordcloud.route("/<string:datafile_id>", methods=["POST", "GET", "DELETE"])
class WordcloudsResource(Resource):
    wc_schema = WordcloudSchema()

    @ns_wordcloud.marshal_with(create_wordcloud_response_model, code=201)
    @error_handler(logger)
    @jwt_required
    def post(self, datafile_id):
        """
            Gera um novo Wordclod
        """
        service = WordcloudAppService(datafile_id)

        create_wc_task = service.create_wordcloud()
        return {
            "create_wc_task_id": create_wc_task.id
        }

    @ns_wordcloud.marshal_with(get_wordclouds_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self, datafile_id):
        """
            Recupera a imagem jpg do Wordcloud gerado, em Base64
        """
        service = WordcloudAppService(datafile_id)
        wc = service.get_wordcloud()
        return self.wc_schema.dump(wc)

    @ns_wordcloud.marshal_with(delete_wordcloud_response_model)
    @error_handler(logger)
    @jwt_required
    def delete(self, datafile_id):
        """
            Exclui o wordcloud
        """
        service = WordcloudAppService(datafile_id)
        deleted = service.delete_wordcloud()

        return {
            "deleted": deleted
        }


@ns_wordcloud.route("/<string:datafile_id>/tasks", methods=["GET"])
class WordCloudsTaskResource(Resource):
    schema = WordcloudCreateTaskSchema()

    @ns_wordcloud.marshal_with(get_wc_tasks_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self, datafile_id):
        """
            Verifica todas as requisições para extração de Wordclouds
        """
        service = WordcloudCreateTaskService(get_current_user())
        tasks = service.list_current_tasks(datafile_id)

        if tasks.count() > 0:
            failed_tasks = service.list_failed_tasks(datafile_id, tasks[tasks.count()-1].created_at)
            return {
                "tasks": self.schema.dump(tasks, many=True),
                "total": tasks.count(False),
                "failed": failed_tasks.count()
            }


