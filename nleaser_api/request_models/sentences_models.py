from flask_restplus import fields, reqparse
from nleaser_api.request_models import make_response_model

###### GET MODELS ######

get_model = reqparse.RequestParser()
get_model.add_argument(
    "datafile_id",
    required=True,
    location="args",
    type=str,
    help="Id do arquivo de dados"
)
get_model.add_argument(
    "skip",
    required=True,
    location="args",
    type=int,
    help="A partir de qual sentença irá retornar (Paginacao)"
)
get_model.add_argument(
    "limit",
    required=True,
    location="args",
    type=int,
    help="Quantidade máxima de sentenças retornadas"
)


sentence_model = {
    "index": fields.Integer(
        required=True,
        description="Representa um indice unico da sentença dentro do arquivo"
    ),
    "content": fields.String(
        required=True,
        description="Conteudo bruto da sentença, representa a sentença enviada pelo usuário"
    ),
    "pre_processed_content": fields.String(
        required=True,
        description="É o conteudo pre-processado da sentença, "
                    "representa a forma mais pura da sentença que será analisado pelos métodos de NLP"
    ),
}

get_response_model = {
    "datafile_id": fields.String(
        description="Identificador unico do arquivo que contém as sentenças"
    ),
    "total": fields.Integer(
        description="Total de sentenças desse arquivo"
    )
}

get_response_model = make_response_model(get_response_model)