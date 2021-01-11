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
    'overwrite',
    required=False,
    location="args",
    type=bool,
    help="Em caso de arquivo duplicado, sobrescreve as informacoes",
    default=False
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
    "hash": fields.String(
        description="Hash de identificação dos dados."
    )
}
post_response_model = make_response_model(post_response_model)