from flask import request
from flask_jwt_extended import jwt_required, get_current_user
from flask_restplus import Namespace, Resource, fields

from api.error_handler import error_handler
from api.request_models.wordcloud_models import get_model, get_response_model, delete_model, delete_response_model, \
    post_model, post_response_model, get_tasks_model, get_tasks_response_model, tasks_model, wordcloud_model

from models.wordcloud import WordcloudSchema
from models.tasks.wordcloud.create import WordcloudCreateTaskSchema
from sources.wordcloud import WordcloudService
from sources.tasks.wordcloud.create import WordcloudCreateTaskService
from sources.logger import create_logger

logger = create_logger(__name__)

ns_wordcloud = Namespace("Wordcloud", "Namespace para criar, verificar e excluir wordclouds")

# POST
create_wordcloud_model = ns_wordcloud.model("create_wordcloud", post_model)
create_wordcloud_response_model = ns_wordcloud.model("create_wordcloud_response_model", post_response_model)

# GET
get_wordclouds_response_model = get_response_model.copy()
get_wordclouds_response_model["wordcloud"] = fields.Nested(
    ns_wordcloud.model("wordcloud_model", wordcloud_model),
    as_list=True, required=False
)
get_wordclouds_response_model = ns_wordcloud.model("get_wordclouds_response_model", get_wordclouds_response_model)

get_wc_tasks_response_model = get_tasks_response_model.copy()
get_wc_tasks_response_model["tasks"] = fields.Nested(
    ns_wordcloud.model("tasks_model", tasks_model),
    as_list=True
)


get_wc_tasks_response_model = ns_wordcloud.model("get_wc_tasks_response_model", get_wc_tasks_response_model)

# DELETE
delete_wordcloud_response_model = ns_wordcloud.model("delete_wordcloud_response_model", delete_response_model)


@ns_wordcloud.route("")
class WordcloudsResource(Resource):
    wc_schema = WordcloudSchema()

    @ns_wordcloud.expect(create_wordcloud_model, validate=False)
    @ns_wordcloud.marshal_with(create_wordcloud_response_model, code=201)
    @error_handler(logger)
    @jwt_required
    def post(self):
        args = request.get_json()
        create_wordcloud_model.validate(args)
        service = WordcloudService(**args)

        create_wc_task = service.create_wordcloud()
        return {
            "create_wc_task_id": create_wc_task.id
        }

    @ns_wordcloud.expect(get_model, validate=False)
    @ns_wordcloud.marshal_with(get_wordclouds_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self):
        args = get_model.parse_args()
        service = WordcloudService(**args)
        wc = service.get_wordcloud()

        return {
            "wordcloud": self.wc_schema.dump(wc) if wc is not None else {}
        }

    @ns_wordcloud.expect(delete_model, validate=False)
    @ns_wordcloud.marshal_with(delete_wordcloud_response_model)
    @error_handler(logger)
    @jwt_required
    def delete(self):
        args = delete_model.parse_args()
        service = WordcloudService(**args)
        deleted = service.delete_wordcloud()

        return {
            "deleted": deleted
        }



@ns_wordcloud.route("/tasks", methods=["GET"])
class WordCloudsTaskResouce(Resource):

    @ns_wordcloud.expect(get_tasks_model, validate=False)
    @ns_wordcloud.marshal_with(get_wc_tasks_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self):
        """
        Verifica todas as requisições para criação de wordclouds que estão em progresso
        :param datafile_id: id do arquivo de dados
        :return: List[WordCloudCreateTask]
        """
        args = get_tasks_model.parse_args()
        service = WordcloudCreateTaskService(get_current_user())
        schema = WordcloudCreateTaskSchema()
        tasks = service.list_current_tasks(**args)
        return {
            "tasks": schema.dump(tasks, many=True),
            "total": tasks.count(False),
            "failed": tasks.filter(status="failed").count(False)
        }
