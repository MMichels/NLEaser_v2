from flask_restplus import Resource, fields

from api.request_models import make_response_model

# POST MODELS
post_model = {
    "email": fields.String(
        required=True,
        description="Email, utilizado para login",
        example="example@email.com"
    ),
    "password": fields.String(
        required=True,
        description="Senha utilizada no login"
    ),
    "name": fields.String(
        required=True,
        description="Nome que será exibido no sistema"
    )
}


post_response_model = {
    "id": fields.Integer(
        description="Id do usuário cadastrado"
    )
}
post_response_model = make_response_model(post_response_model)