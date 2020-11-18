from flask_restplus import Api
from .namespaces.ns_users import ns_users
from .namespaces.ns_authentication import ns_authentication

api = Api(
    title="NLEaser",
    description="Aplicação voltada a facilitar o acesso a recursos de NLP"
)

api.authorizations = {
    "apiKey": {
        "type": 'apiKey',
        "in": "header",
        "name": "Authorization"
    }
}
api.security = "apiKey"
api.add_namespace(ns_users, path="/user")
api.add_namespace(ns_authentication, path="/login")
