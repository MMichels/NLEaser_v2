from flask_restplus import fields


default_response_model = {
    "status": fields.String(
        required=True,
        description="Identifica se a requisição foi processada com sucesso ou se houveram erros",
        example="success",
        default="success"
    ),
    "error": fields.String(
        required=False,
        description="Se o status for diferente de \"success\" esse campo irá conter uma mensagem amigavel " +
                    "sobre o erro ocorrido",
        example="Ops, Houve um erro desconhecido no servidor, se o erro persistir, contate o suporte"
    ),
    "messages": fields.Wildcard(
        fields.String,
        required=False,
        description="Se o status for \"validation_error\" esse campo irá conter as mensagens de erro de validação"
    )
}


def make_response_model(model: dict) -> dict:
    updated_model = model.copy()
    updated_model.update(default_response_model)
    return updated_model