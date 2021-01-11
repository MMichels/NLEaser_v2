from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource

from api.error_handler import error_handler
from api.request_models.data_management_api_models import post_model, post_response_model

from sources.logger import create_logger
from sources.datafile import import_data_file

from mongoengine.errors import NotUniqueError
from sources.datafile.exceptions import InvalidFormatException, FileReadException, TextColumnNotFound

logger = create_logger(__name__)

ns_data_management = Namespace(
    "Data Management",
    "Namespace para enviar, alterar, excluir e recuperar os datasets do usuário"
)

upload_response_model = ns_data_management.model("upload_response_model", post_response_model)


@ns_data_management.route("")
class DataManagementResource(Resource):

    @ns_data_management.expect(post_model, validate=False)
    @ns_data_management.marshal_with(upload_response_model, code=201)
    @error_handler(logger)
    @jwt_required
    def post(self):
        args = post_model.parse_args()
        try:
            datafile = import_data_file(**args)
            return {
                'hash': datafile.hash
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


    @error_handler(logger)
    def get(self):
        return 200

    @error_handler(logger)
    def put(self):
        return 200

    @error_handler(logger)
    def delete(self):
        return 200
