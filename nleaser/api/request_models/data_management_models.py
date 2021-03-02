from flask_restplus import fields, reqparse
from werkzeug.datastructures import FileStorage
from nleaser.api.request_models import make_response_model

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
        description="Id unico do arquivo no banco de dados"
    )
}
post_response_model = make_response_model(post_response_model)

###### GET MODELS ######
datafile_model = {
    "id": fields.String(
        required=True,
        description="É o ID unico que identifica esse arquivo no banco de dados"
    ),
    "name": fields.String(
        required=True,
        description="É o nome do arquivo enviado pelo usuário"
    ),
    "language": fields.String(
        required=True,
        description="É o idioma do arquivo informado pelo usuário, "
                    "utilizado por alguns métodos de NLP durante as analises"
    ),
    "text_column": fields.String(
        required=False,
        default="txt",
        description="Representa a coluna que contem as sentenças dentro do arquivo (csv, excel)"
    ),
    "created_at": fields.DateTime(
        required=True,
        description="É a data em que foi realizado o uploaad do arquivo"
    ),
}

get_response_model = make_response_model(datafile_model)

get_list_model = reqparse.RequestParser()
get_list_model.add_argument(
    "orderby",
    required=True,
    location="args",
    type=str,
    help="Campo utilizado para ordernar a lista de resultados",
    choices=["name", "created_at"],
)
get_list_model.add_argument(
    "order_ascending",
    default=True,
    required=False,
    location="args",
    type=bool,
    help="Ordernar os resultados de forma ascendente"
)

list_datafile_response_model = {
    "total": fields.Integer(
        required=True,
        description="Corresponde ao numero total de documentos que o usuário possui"
    )
}

list_datafile_response_model = make_response_model(list_datafile_response_model)

##### DELETE MODELS
delete_response_model = {
    "deleted": fields.Boolean(
        required=True,
        description="Confirma se o arquivo foi excluido ou não"
    )
}
delete_response_model = make_response_model(delete_response_model)
