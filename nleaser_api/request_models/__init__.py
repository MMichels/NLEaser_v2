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


##### TASKS MODELS #####
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
    "total": fields.Integer(
        required=True,
        description="Total de passos necessários para concluir a tarefa"
    ),
    "progress": fields.Integer(
        required=True,
        description="Passo atual da tarefa"
    ),
    "error": fields.String(
        required=False,
        description="identifica se ocorreu algum erro"
    )
}