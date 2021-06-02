from importlib.resources import Resource

from flask_jwt_extended import jwt_required, get_current_user
from flask_restplus import Namespace, fields

from nleaser.api.error_handler import error_handler
from nleaser.api.request_models import get_tasks_response_model, tasks_model
from nleaser.api.request_models.ner_models import post_response_model, get_response_model, entity_model, \
    delete_response_model, get_model
from nleaser.models.nlp_extracted_data.ner import NerResumeSchema
from nleaser.models.tasks.ner.create_resume import NerResumeCreateTaskSchema
from nleaser.sources.logger import create_logger
from nleaser.sources.ner import NerResumeService
from nleaser.sources.tasks.ner.create_resume import NerResumeCreateTaskService

logger = create_logger(__name__)
ns_ner = Namespace(
    "NerResume",
    "Namespace para extrair, paginar e excluir um resumo sobre as entidades de um conjunto de dados"
)

# POST
create_ner_resume_response_model = ns_ner.model(
    "create_ner_resume_response_model", post_response_model
)

# GET
get_ner_resume_response_model = get_response_model.copy()
get_ner_resume_response_model["entities"] = fields.Nested(
    ns_ner.model("entity_model", entity_model), as_list=True
)
get_ner_resume_response_model = ns_ner(
    "get_ner_resume_response_model", get_ner_resume_response_model
)

# DELETE
delete_ner_resume_response_model = ns_ner.model(
    "delete_ner_resume_response_model", delete_response_model
)

# TASKS
get_ner_resume_tasks_response_model = get_tasks_response_model.copy()
get_ner_resume_tasks_response_model["tasks"] = fields.Nested(
    ns_ner.model("ner_resume_tasks_model", tasks_model), as_list=True
)
get_ner_resume_tasks_response_model = ns_ner.model(
    "get_ner_resume_tasks_response_model", get_ner_resume_tasks_response_model
)


@ns_ner.route("/<string:datafile_id>", methods=["POST", "GET", "DELETE"])
class NerResource(Resource):
    ner_resume_schema = NerResumeSchema()

    @ns_ner.marshal_with(create_ner_resume_response_model, code=201)
    @error_handler(logger)
    @jwt_required
    def post(self, datafile_id: str):
        """
            Extrair um novo resumo das entidades do dataset
        """
        service = NerResumeService(datafile_id)
        create_ner_resume_task = service.create_ner_resume()
        return {
            'create_ner_resume_response_model': create_ner_resume_task.id
        }

    @ns_ner.expect(get_model, validate=False)
    @ns_ner.marshal_with(get_ner_resume_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self, datafile_id):
        """
            Realiza a paginação entre as entidades extraidas
        """
        args = get_model.parse_args()
        service = NerResumeService(datafile_id)
        ner_resume = service.get_ner_resume(**args)
        return self.ner_resume_schema.dump(ner_resume)

    @ns_ner.marshal_with(delete_ner_resume_response_model)
    @error_handler(logger)
    @jwt_required
    def delete(self, datafile_id):
        """
            Exclui as entidades extraidas
        """
        service = NerResumeService(datafile_id)
        deleted = service.delete_ner_resume()
        return {
            "deleted": deleted
        }


@ns_ner.route("/<string:datafile_id>/tasks", methods=["GET"])
class NerResumeTaskResource(Resource):
    schema = NerResumeCreateTaskSchema()

    @ns_ner.marshal_with(get_ner_resume_tasks_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self, datafile_id):
        """
            Verifica todas as requisições de extração de entidades
        """
        service = NerResumeCreateTaskService(get_current_user())
        tasks = service.list_current_tasks(datafile_id)

        if tasks.count() > 0:
            failed_tasks = service.list_failed_tasks(datafile_id, tasks[tasks.count() - 1].created_at)
            return {
                "tasks": self.schema.dump(tasks, many=True),
                "total": tasks.count(False),
                "failed": failed_tasks.count()
            }
