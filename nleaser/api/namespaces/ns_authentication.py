from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource, Model

from nleaser.api.error_handler import error_handler
from nleaser.api.request_models.authentication_models import post_model, post_response_model

from nleaser.sources.authentication import AuthenticationService
from nleaser.sources.logger import create_logger

logger = create_logger(__name__)

ns_authentication = Namespace("Authentication", "Namespace para autenticação dos usuarios")

login_model: Model = ns_authentication.model("login_model", post_model)
login_response_model = ns_authentication.model("login_response_model", post_response_model)


@ns_authentication.route("")
class LoginResource(Resource):

    @ns_authentication.expect(login_model, validate=False)
    @ns_authentication.marshal_with(login_response_model, code=201)
    @ns_authentication.doc(security=None)
    @error_handler(logger)
    def post(self):
        args = request.get_json()
        login_model.validate(args)

        service = AuthenticationService()
        token = service.authenticate(**args)

        if token:
            return {
                "access_token": token
            }

        else:
            return {
                       "status": "login_failed",
                       "error": "Login ou senha inválidos, tente novamente"
                   }, 401

    @jwt_required
    def get(self):
        service = AuthenticationService()

        return {
            "logged_as": service.get_current_user(),
        }
