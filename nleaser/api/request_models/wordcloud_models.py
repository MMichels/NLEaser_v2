from flask_restplus import fields, reqparse
from nleaser.api.request_models import make_response_model


##### POST MODELS #####
post_response_model = {
    "create_wc_task_id": fields.String(
        required=True,
        description="Id da task que representa a criação desse wc"
    )
}

post_response_model = make_response_model(post_response_model)

##### GET MODELS #####
wordcloud_model = {
    "base64_image": fields.String(
        required=True,
        description="Imagem codificada em base64"
    ),
    "created_at": fields.DateTime(
        required=True,
        description="Data e hora em que o wordcloud foi criado"
    )
}
get_response_model = make_response_model(wordcloud_model)

##### DELETE MODELS #####
delete_response_model = {
    "deleted": fields.Boolean(
        required=True,
        description="indica se o wc foi excluido"
    )
}
delete_response_model = make_response_model(delete_response_model)
