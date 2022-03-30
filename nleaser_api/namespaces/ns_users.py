from flask import request
from flask_restplus import Namespace, Resource, Model

from nleaser_api.error_handler import error_handler
from nleaser_api.request_models.user_models import post_model, post_response_model

from nleaser_sources.app_services.user import UserAppService
from nleaser_sources.logger import create_logger

from mongoengine.errors import NotUniqueError

logger = create_logger(__name__)

ns_users = Namespace("Users", "Namespace para criar os usuarios", authorizations="apiKey")

create_user_model: Model = ns_users.model("create_user_model", post_model)
create_user_response_model = ns_users.model("create_user_response_model", post_response_model)


@ns_users.route("")
class UsersResource(Resource):
    service = UserAppService()

    @error_handler(logger)
    @ns_users.expect(create_user_model, validate=False)
    @ns_users.marshal_with(create_user_response_model, code=201)
    @ns_users.doc(security=None)
    def post(self):
        args = request.get_json()
        create_user_model.validate(args)
        try:
            new_user = self.service.create_new_user(**args)
            return {'id': str(new_user.id)}, 201
        except NotUniqueError as nu:
            return {
                       "status": "alrealy_exists",
                       "error": "Já existe um usuário com o email " + args['email']
                   }, 409
