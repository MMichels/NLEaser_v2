from flask_jwt_extended import jwt_required, get_current_user
from flask_restplus import Namespace, fields, Resource

from nleaser_api.error_handler import error_handler
from nleaser_api.request_models import get_tasks_response_model, tasks_model
from nleaser_api.request_models.ner_models import post_response_model, get_response_model, entity_model, \
    delete_response_model, get_model

from nleaser_models.nlp.ner import NerResumeSchema
from nleaser_models.tasks.ner import NerResumeCreateTaskSchema

from nleaser_sources.app_services.ner import NerResumeAppService
from nleaser_sources.app_services.tasks.ner import NerResumeCreateTaskService
from nleaser_sources.logger import create_logger

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
get_ner_resume_response_model["extracted_entities"] = fields.Nested(
    ns_ner.model("entity_model", entity_model), as_list=True
)
get_ner_resume_response_model = ns_ner.model(
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
        service = NerResumeAppService(datafile_id)
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
        service = NerResumeAppService(datafile_id)
        ner_resume = service.get_ner_resume(**args)
        return self.ner_resume_schema.dump(ner_resume)

    @ns_ner.marshal_with(delete_ner_resume_response_model)
    @error_handler(logger)
    @jwt_required
    def delete(self, datafile_id):
        """
            Exclui as entidades extraidas
        """
        service = NerResumeAppService(datafile_id)
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
