from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource, Model

from api.error_handler import error_handler
from api.request_models.user_api_models import post_model, post_response_model

from sources.user import create_new_user
from sources.logger import create_logger


logger = create_logger(__name__)

ns_users = Namespace("Users", "Namespace para criar os usuarios", authorizations="apiKey")

create_user_model: Model = ns_users.model("create_user_model", post_model)
create_user_response_model = ns_users.model("create_user_response_model", post_response_model)


@ns_users.route("")
class UsersResource(Resource):

    @error_handler(logger)
    @ns_users.expect(create_user_model, validate=False)
    @ns_users.marshal_with(create_user_response_model, code=201)
    @ns_users.doc(security=None)
    def post(self):
        args = request.get_json()
        create_user_model.validate(args)
        new_user = create_new_user(**args)
        return new_user.id, 201
