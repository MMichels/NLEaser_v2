from flask_restplus import Api
from .ns_users import ns_users
from .ns_authentication import ns_authentication
from .ns_data_management import ns_data_management
from .ns_sentences import ns_sentences
from .ns_wordcloud import ns_wordcloud

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
api.add_namespace(ns_data_management, path="/datafile")
api.add_namespace(ns_sentences, path="/sentences")
api.add_namespace(ns_wordcloud, path="/wordcloud")