from flask_restplus import fields, reqparse
from werkzeug.datastructures import FileStorage
from api.request_models import make_response_model

##### POST MODELS ########
post_model = reqparse.RequestParser()
post_model.add_argument(
    'file',
    required=True,
    location='files',
    type=FileStorage,
    help="Arquivo com as sentenças."
)
post_model.add_argument(
    'format',
    required=True,
    location="args",
    type=str,
    choices=["csv", "xlsx", "txt"],
    help="Formato do arquivo."
)
post_model.add_argument(
    'text_column',
    required=True,
    location="args",
    type=str,
    help="Coluna que contém as sentenças"
)
post_model.add_argument(
    'language',
    required=True,
    location="args",
    type=str,
    help="Idioma das frases do arquivo"
)
post_model.add_argument(
    'separador',
    required=False,
    location="args",
    type=str,
    help="Informa qual o caractere utilizado para separar as colunas",
    default=";"
)

post_response_model = {
    "id": fields.String(
        description="Hash de identificação dos dados."
    )
}
post_response_model = make_response_model(post_response_model)

###### GET MODELS
get_model = reqparse.RequestParser()
get_model.add_argument(
    "orderby",
    required=True,
    location="args",
    type=str,
    help="Campo utilizado para ordernar a lista de resultados",
    choices=["name", "created_at"],
)
get_model.add_argument(
    "order_ascending",
    default=True,
    required=False,
    location="args",
    type=bool,
    help="Ordernar os resultados de forma ascendente"
)


datafile_model = {
    "id": fields.String(),
    "name": fields.String(),
    "language": fields.String(),
    "text_column": fields.String(),
    "created_at": fields.DateTime(),
}

get_response_model = {
    "total": fields.Integer()
}

get_response_model = make_response_model(get_response_model)


##### DELETE MODELS
delete_model = reqparse.RequestParser()
delete_model.add_argument(
    "id",
    required=True,
    location="args",
    type=str,
    help="Identificador do arquivo"
)


delete_response_model = {
    "deleted": fields.Boolean()
}
delete_response_model = make_response_model(delete_response_model)