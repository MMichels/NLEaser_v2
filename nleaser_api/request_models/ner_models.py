from flask_restplus import reqparse, fields
from nleaser_api.request_models import make_response_model

##### POST MODELS #####
post_response_model = {
    "create_ner_resume_task_id": fields.String(
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
    default="count",
    choices=["content", "count", "entity"],
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

entity_model = {
    'content': fields.String(
        required=True,
        description="Texto extraido"
    ),
    'entity': fields.String(
        required=True,
        description="Nome da entidade"
    ),
    'count': fields.Integer(
        required=True,
        description="Quantidade de vezes que essa entidade apareceu no conjunto de dados"
    )
}

ner_resume_model = {
    'datafile': fields.String(
        required=True,
        description="Id do datafile referente a essa extração de entidades"
    ),
    'created_at': fields.DateTime(
        required=True,
        description="Data e hora que o reumo foi extraido"
    ),
    'total': fields.Integer(
        required=True,
        description="Total de entidades encontradas"
    )
}

get_response_model = make_response_model(ner_resume_model)

##### DELETE MODELS #####
delete_response_model = {
    "deleted": fields.Boolean(
        required=True,
        description="indica se o registro de entidades foi excluido"
    )
}
delete_response_model = make_response_model(delete_response_model)
