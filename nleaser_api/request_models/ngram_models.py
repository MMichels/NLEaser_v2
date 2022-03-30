from flask_restplus import reqparse, fields
from nleaser_api.request_models import make_response_model

##### POST MODELS #####

post_model = reqparse.RequestParser()
post_model.add_argument(
    'size',
    required=True,
    location='args',
    type=int,
    choices=[1, 2, 3, 4],
    help="Quantidade de palavras para considerar (tamanho do gram)"
)

post_response_model = {
    "create_ngram_task_id": fields.String(
        description="Id da requisição na fila"
    )
}
post_response_model = make_response_model(post_response_model)

##### GET MODELS #####
get_model = reqparse.RequestParser()
get_model.add_argument(
    "skip",
    required=True,
    location="args",
    type=int,
    help="A partir de qual registro irá retornar (Paginacao)"
)
get_model.add_argument(
    "limit",
    required=True,
    location="args",
    type=int,
    help="Quantidade máxima de sentenças retornadas"
)
get_model.add_argument(
    "order_by",
    required=False,
    default="relevance",
    choices=["content", "count", "relevance"],
    location="args",
    type=str,
    help="Indica se irá ordenar os ngrams por conteudo, quantidade ou relevancia"
)
get_model.add_argument(
    "order_ascending",
    required=False,
    default=0,
    choices=[0, 1],
    type=int,
    location='args',
    help="Define se irá ordenar de forma ascendente ou descendente"
)

ngram_model = {
    'content': fields.String(
        required=True,
        description="Palavras que compõe esse ngram"
    ),
    'count': fields.Integer(
        required=True,
        description="Quantidade de vezes que esse ngram ocorreu"
    ),
    'relevance': fields.Float(
        required=True,
        description="Indica a relevancia desse Ngram em relação ao conjunto de dados"
    )
}

ngrams_model = {
    'datafile': fields.String(
        required=True,
        description="Id do datafile referente a esses NGrams"
    ),
    "created_at": fields.DateTime(
        required=True,
        description="Data e hora em que o wordcloud foi criado"
    ),
    'size': fields.Integer(
        required=True,
        description="Tamanho dos grams analisados"
    ),
    'total': fields.Integer(
        required=True,
        description="Total de ngrams extraidos"
    )
}

get_response_model = make_response_model(ngrams_model)

##### DELETE MODELS #####
delete_response_model = {
    "deleted": fields.Boolean(
        required=True,
        description="indica se o ngram foi excluido"
    )
}

delete_response_model = make_response_model(delete_response_model)
