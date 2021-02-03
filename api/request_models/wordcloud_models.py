from flask_restplus import fields, reqparse
from api.request_models import make_response_model


##### POST MODELS #####
post_model = {
    "datafile_id": fields.String(
        required=True,
        description="id do arquivo de sentenças para gerar o wordcloud"
    )
}

post_response_model = {
    "create_wc_task_id": fields.String(
        required=True,
        description="Id da task que representa a criação desse wc"
    )
}

post_response_model = make_response_model(post_response_model)

##### GET MODELS #####
get_model = reqparse.RequestParser()
get_model.add_argument(
    "datafile_id",
    required=True,
    location="args",
    type=str,
    help="id do arquivo de sentenças"
)

get_response_model = {
    "wordcloud": fields.String(
        required=True,
        description="o wordcloud mais recente encodado em base64"
    )
}

##### DELETE MODELS #####
delete_model = reqparse.RequestParser()
delete_model.add_argument(
    "datafile_id",
    required=True,
    location="args",
    type=str,
    help="id do arquivo de sentenças"
)


delete_response_model = {
    "deleted": fields.Boolean(
        required=True,
        description="indica se o wc foi excluido"
    )
}
delete_response_model = make_response_model(delete_response_model)

##### TASKS MODELS #####
get_tasks_model = reqparse.RequestParser()
get_tasks_model.add_argument(
    "datafile_id",
    required=True,
    location="args",
    type=str,
    help="id do arquivo de sentenças"
)

get_tasks_response_model = {
    "total": fields.Integer(
        required=True,
        decription="total de wordcloud tasks encontradas para esse arquivo"
    ),
    "failed": fields.Integer(
        required=True,
        description="total de wordcloud tasks que apresentam falhas para esse arquivo"
    )
}
get_tasks_response_model = make_response_model(get_tasks_response_model)

tasks_model = {
    "id": fields.String(
        required=True,
        description="id da task"
    ),
    "created_at": fields.DateTime(
        required=True,
        description="data de criação da task"
    ),
    "status": fields.String(
        required=True,
        decription="Status da task"
    ),
    "error": fields.String(
        required=False,
        description="identifica se ocorreu algum erro"
    )
}