from flask_restplus import reqparse, fields

##### POST MODELS #####
from nleaser.api.request_models import make_response_model

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
