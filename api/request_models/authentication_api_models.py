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
        description="Senha utilizada no login",
        example="senha123"
    )
}


post_response_model = {
    "access_token": fields.String(
        description="Token de acesso JWT utilizado para realizar as proximas requisições"
    )
}
post_response_model = make_response_model(post_response_model)