from functools import wraps
from logging import Logger

from flask import request
from werkzeug.exceptions import BadRequest
from marshmallow.exceptions import ValidationError


def error_handler(logger: Logger):
    def handled_function(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except BadRequest as e:
                logger.error(
                    "Os dados recebidos estão fora do padrão do endpoint",
                    exc_info=True,
                    extra={"received_args": request.get_json()}
                )
                return {
                           "status": "bad_request",
                           "error": "Ops, as informações que o servidor recebeu estão diferente do esperado, " +
                                    "se o erro persistir contate o suporte",
                           "messages": e.data["errors"]
                       }, 400

            except ValidationError as ve:
                logger.error(
                    "Erro ao validar informações e carregar os modelos",
                    exc_info=True,
                    extra={"received_args": request}
                )
                return {
                    "status": "validation_error",
                    "error": "Durante a validação das informações, alguns problemas ocorreram, " +
                             "se o erro persistir contate o suporte",
                    "messages": ve.normalized_messages()
                }

            except FileNotFoundError as fn:
                return {
                           "status": "not_found",
                           "error": fn.args[0]
                       }, 404

            except Exception as e:
                logger.error(
                    "Ocorreu um erro desconhecido no servidor",
                    exc_info=True,
                    extra={"received_args": request}
                )
                return {
                           "status": "error",
                           "error": "Ops! parece que você encontrou uma falha..." +
                                    "Se o erro persistir contate o suporte e iremos colocar o estagiário para resolver."
                       }, 500

        return wrap

    return handled_function
