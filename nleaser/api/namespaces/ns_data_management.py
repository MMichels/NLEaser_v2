from flask_jwt_extended import jwt_required, get_current_user
from flask_restplus import Namespace, Resource, Model, fields

from nleaser.api.error_handler import error_handler
from nleaser.api.request_models import tasks_model, get_tasks_response_model
from nleaser.api.request_models.data_management_models import datafile_model, delete_response_model, \
    get_list_model, get_response_model, list_datafile_response_model, post_model, post_response_model

from nleaser.models.datafile import DataFileSchema
from nleaser.models.tasks.datafile.upload import DataFileUploadTaskSchema
from nleaser.sources.logger import create_logger
from nleaser.sources.datafile import DataFileService


from mongoengine.errors import NotUniqueError
from nleaser.sources.datafile.exceptions import InvalidFormatException, FileReadException, TextColumnNotFound, NotAuthorized
from nleaser.sources.tasks.datafile.upload import DataFileUploadTaskService

logger = create_logger(__name__)

ns_data_management = Namespace(
    "Data Management",
    "Namespace para enviar, alterar, excluir e recuperar os datasets do usuário"
)

# POST
upload_response_model: Model = ns_data_management.model("upload_response_model", post_response_model)

# GET
get_datafile_response_model: Model = ns_data_management.model("get_datafile_response_model", get_response_model, mask=None)

list_datafiles_response_model = list_datafile_response_model.copy()
list_datafiles_response_model["documents"] = fields.Nested(
    ns_data_management.model("datafile_response_model", datafile_model, mask=None),
    as_list=True, mask=None
)

list_datafiles_response_model: Model = ns_data_management.model(name="list_datafiles_response_model",
                                                                model=list_datafiles_response_model,
                                                                mask=None)

# DELETE
delete_datafile_response_model: Model = ns_data_management.model("delete_datafile_response_model",
                                                                 delete_response_model)

# TASKS
get_df_tasks_response_model = get_tasks_response_model.copy()
get_df_tasks_response_model["tasks"] = fields.Nested(
    ns_data_management.model("task_model", tasks_model), as_list=True
)
get_df_tasks_response_model = ns_data_management.model(
    "get_df_tasks_response_model", get_df_tasks_response_model
)


@ns_data_management.route("")
class DataManagementResource(Resource):
    schema = DataFileSchema()

    @ns_data_management.expect(post_model, validate=False)
    @ns_data_management.marshal_with(upload_response_model, code=201)
    @error_handler(logger)
    @jwt_required
    def post(self):
        """
        Realiza o upload de um novo arquivo.
        """
        args = post_model.parse_args()
        service = DataFileService()
        try:
            datafile = service.import_datafile(**args)
            return {
                'id': datafile.id
            }
        except NotUniqueError:
            return {
                       'status': 'alrealy_exists',
                       'error': 'Você ja realizou o upload deste arquivo.'
                   }, 409
        except TextColumnNotFound as e:
            return {
                       "status": "column_not_found",
                       "error": e.args[0]
                   }, 409
        except FileReadException as fre:
            logger.error(
                "Ocorreu um erro ao ler o arquivo do usuário",
                exc_info=True,
                extra={"received_args": args}
            )
            return {
                       'status': "file_read_error",
                       "error": "Ocorreu um erro ao ler o arquivo, isso normalmente é causado por um arquivo mal formatado, "
                                "corrompido ou então um formato não suportado até o momento"
                   }, 415
        except InvalidFormatException as fie:
            logger.error(
                "O formato de arquivo informado não é suportado no momento",
                exc_info=True,
                extra={"received_args": args}
            )
            return {
                       'status': "invalid_format",
                       "error": "Desculpe, mas atualmente não fornecemos suporte ao tipo de arquivo informado, "
                                "converta seu arquivo para um dos formatos suportados e tente novamente."
                   }, 415

    @ns_data_management.expect(get_list_model, validate=False)
    @ns_data_management.marshal_with(list_datafiles_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self):
        """
        Retorna a lista de arquivos desse usuario
        """
        args = get_list_model.parse_args()
        service = DataFileService()

        documents = service.list_all_datafiles(**args)

        result = {
            "documents": self.schema.dump(documents, many=True),
            "total": documents.count()
        }

        return result


@ns_data_management.route("/<string:datafile_id>")
class DataManagementSingleResource(Resource):
    schema = DataFileSchema()

    @ns_data_management.marshal_with(get_datafile_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self, datafile_id):
        """
        Retorna as informações de apenas 1 arquivo
        Args:
            datafile_id: id do arquivo que vc deseja obter
        """

        service = DataFileService()
        document = service.get_datafile(datafile_id)
        return self.schema.dump(document)

    @ns_data_management.marshal_with(delete_datafile_response_model)
    @error_handler(logger)
    @jwt_required
    def delete(self, datafile_id):
        """
        Exclui o arquivo
        """
        service = DataFileService()

        try:
            deleted = service.delete_datafile(datafile_id)
            return {
                "deleted": deleted
            }
        except NotAuthorized:
            return {
                       "status": "not_authorized",
                       "error": "Você não possui autorização para excluir esse arquivo"
                   }, 403


@ns_data_management.route("/<string:datafile_id>/tasks")
class DataManagementTaskResource(Resource):
    schema = DataFileUploadTaskSchema()

    @ns_data_management.marshal_with(get_df_tasks_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self, datafile_id):
        """
        Retorna a as tarefas de upload relacionadas a esse arquivo (progresso do upload)
        """
        service = DataFileUploadTaskService(get_current_user())
        tasks = service.list_current_tasks(datafile_id)

        if tasks.count() > 0:
            failed_tasks = service.list_failed_tasks(datafile_id, tasks[tasks.count()-1].created_at)
            return {
                "tasks": self.schema.dump(tasks, many=True),
                "total": tasks.count(False),
                "failed": failed_tasks.count()
            }