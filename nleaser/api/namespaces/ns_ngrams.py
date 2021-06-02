from flask_jwt_extended import jwt_required, get_current_user
from flask_restplus import Namespace, Resource, fields

from nleaser.api.error_handler import error_handler
from nleaser.api.request_models import get_tasks_response_model, tasks_model
from nleaser.api.request_models.ngram_models import post_model, post_response_model, get_response_model, \
    delete_response_model, ngram_model, get_model
from nleaser.models.nlp_extracted_data.ngrams import ExtractedNGramsSchema
from nleaser.models.tasks.ngrams.create import NGramsCreateTaskSchema
from nleaser.sources.logger import create_logger
from nleaser.sources.ngrams import NGramsService
from nleaser.sources.tasks.ngrams.create import NGramsCreateTaskService

logger = create_logger(__name__)
ns_ngrams = Namespace(
    "NGrams",
    "Namespace para extrair, paginar e excluir NGrams dos conjuntos de dados"
)

# POST
create_ngram_response_model = ns_ngrams.model(
    "create_ngram_response_model", post_response_model
)

# GET
get_ngram_response_model = get_response_model.copy()
get_ngram_response_model["ngrams"] = fields.Nested(
    ns_ngrams.model("ngram_model", ngram_model), as_list=True
)
get_ngram_response_model = ns_ngrams.model(
    "get_ngram_response_model", get_ngram_response_model
)

# DELETE
delete_ngram_response_model = ns_ngrams.model("delete_ngram_response_model", delete_response_model)

# TASKS
get_ngrams_tasks_response_model = get_tasks_response_model.copy()
get_ngrams_tasks_response_model["tasks"] = fields.Nested(
    ns_ngrams.model("ngrams_tasks_model", tasks_model), as_list=True
)
get_ngrams_tasks_response_model = ns_ngrams.model("get_ngrams_tasks_response_model", get_ngrams_tasks_response_model)


@ns_ngrams.route("/<string:datafile_id>", methods=["POST", "GET", "DELETE"])
class NGramsResource(Resource):
    ngrams_schema = ExtractedNGramsSchema()

    @ns_ngrams.expect(post_model, validate=False)
    @ns_ngrams.marshal_with(create_ngram_response_model, code=201)
    @error_handler(logger)
    @jwt_required
    def post(self, datafile_id: str):
        """
            Extrai os Ngrams de um conjunto de dados
        """
        args = post_model.parse_args()
        service = NGramsService(datafile_id)
        create_ngram_task = service.create_ngram(**args)
        return {
            "create_ngram_task_id": create_ngram_task.id
        }

    @ns_ngrams.expect(get_model, validate=False)
    @ns_ngrams.marshal_with(get_ngram_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self, datafile_id):
        """
            Realizar a paginação entre os ngrams extraidos
        """
        args = get_model.parse_args()
        service = NGramsService(datafile_id)
        ngram = service.get_ngram(**args)
        return self.ngrams_schema.dump(ngram)

    @ns_ngrams.marshal_with(delete_ngram_response_model)
    @error_handler(logger)
    @jwt_required
    def delete(self, datafile_id):
        """
            Exclui o ngram
        """
        service = NGramsService(datafile_id)
        deleted = service.delete_ngram()
        return {
            "deleted": deleted
        }


@ns_ngrams.route("/<string:datafile_id>/tasks", methods=["GET"])
class NGramsTaskResource(Resource):
    schema = NGramsCreateTaskSchema()

    @ns_ngrams.marshal_with(get_ngrams_tasks_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self, datafile_id):
        """
            Verifica as todas as requisições de extração de NGrams
        """
        service = NGramsCreateTaskService(get_current_user())
        tasks = service.list_current_tasks(datafile_id)

        if tasks.count() > 0:
            failed_tasks = service.list_failed_tasks(datafile_id, tasks[tasks.count() - 1].created_at)
            return {
                "tasks": self.schema.dump(tasks, many=True),
                "total": tasks.count(False),
                "failed": failed_tasks.count()
            }
