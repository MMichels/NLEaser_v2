from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource, Model, fields

from nleaser.api.error_handler import error_handler
from nleaser.api.request_models.data_management_models import datafile_model, delete_model, delete_response_model, \
    get_model, get_response_model, \
    post_model, post_response_model

from nleaser.models.datafile import DataFileSchema
from nleaser.sources.logger import create_logger
from nleaser.sources.datafile import DataFileService


from mongoengine.errors import NotUniqueError
from nleaser.sources.datafile.exceptions import InvalidFormatException, FileReadException, TextColumnNotFound, NotAuthorized

logger = create_logger(__name__)

ns_data_management = Namespace(
    "Data Management",
    "Namespace para enviar, alterar, excluir e recuperar os datasets do usuário"
)

# POST
upload_response_model: Model = ns_data_management.model("upload_response_model", post_response_model)

# GET

list_datafiles_response_model = get_response_model.copy()
list_datafiles_response_model["documents"] = fields.Nested(
    ns_data_management.model("datafile_model", datafile_model, mask=None),
    as_list=True, mask=None
)

list_datafiles_response_model: Model = ns_data_management.model(name="list_datafiles_response_model",
                                                                model=list_datafiles_response_model,
                                                                mask=None)

# DELETE
delete_datafile_response_model: Model = ns_data_management.model("delete_datafile_response_model",
                                                                 delete_response_model)


@ns_data_management.route("")
class DataManagementResource(Resource):
    schema = DataFileSchema()

    @ns_data_management.expect(post_model, validate=False)
    @ns_data_management.marshal_with(upload_response_model, code=201)
    @error_handler(logger)
    @jwt_required
    def post(self):
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

    @ns_data_management.expect(get_model, validate=False)
    @ns_data_management.marshal_with(list_datafiles_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self):
        args = get_model.parse_args()
        service = DataFileService()

        documents = service.list_all_datafiles(**args)

        result = {
            "documents": self.schema.dump(documents, many=True),
            "total": documents.count()
        }

        return result

    @ns_data_management.expect(delete_model, validate=False)
    @ns_data_management.marshal_with(delete_datafile_response_model)
    @error_handler(logger)
    @jwt_required
    def delete(self):
        args = delete_model.parse_args()
        service = DataFileService()

        try:
            deleted = service.delete_datafile(**args)
            return {
                "deleted": deleted
            }
        except NotAuthorized:
            return {
                       "status": "not_authorized",
                       "error": "Você não possui autorização para excluir esse arquivo"
                   }, 403
