from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restplus import Namespace, Resource, Model

from api.error_handler import error_handler
from api.request_models.authentication_api_models import post_model, post_response_model
from models.user import UserSchema

from sources.authentication import authenticate
from sources.logger import create_logger

logger = create_logger(__name__)

ns_authentication = Namespace("Authentication", "Namespace para autenticação dos usuarios")

login_model: Model = ns_authentication.model("login_model", post_model)
login_response_model = ns_authentication.model("login_response_model", post_response_model)


@ns_authentication.route("")
class LoginResource(Resource):
    schema = UserSchema()

    @ns_authentication.expect(login_model)
    @ns_authentication.marshal_with(login_response_model, code=200)
    @ns_authentication.doc(security=None)
    @error_handler(logger)
    def post(self):
        args = request.get_json()
        login_model.validate(args)

        user = authenticate(args["email"], args["password"])

        if user:
            access_token = create_access_token(self.schema.dump(user))
            return {
                "access_token": access_token
            }

        else:
            return {
                       "status": "login_failed",
                       "error": "Login ou senha inválidos, tente novamente"
                   }, 401

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        return {
            "logged_as": current_user,
        }


