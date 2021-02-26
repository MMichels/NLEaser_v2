import mongoengine as me
from nleaser.models.config import ConfigModel


class RabbitQueueModel(me.EmbeddedDocument):
    exchange = me.StringField(required=True)
    queue = me.StringField(required=True)
    routing_key = me.StringField(required=True)


class RabbitQueueConfigModel(ConfigModel):
    cripted = me.fields.BooleanField(default=False)
    value = me.fields.EmbeddedDocumentField(RabbitQueueModel, required=True)


if __name__ == '__main__':
    from nleaser.models import connect_db

    connect_db()

    while True:
        exchange = input("Nome da exchange: ")
        queue = input("Nome da queue: ")
        routing_key = f"{exchange}.{queue}"

        rqm = RabbitQueueModel(
            exchange=exchange,
            queue=queue,
            routing_key=routing_key
        )

        cfg = RabbitQueueConfigModel(
            name=routing_key,
            value=rqm
        )

        try:
            cfg.save()
            print("Salvo!")
        except Exception as ex:
            print("Erro ao salvar: ", ex)

        interromper = input("Continuar? (s/n)").lower()[0] == 'n'
        if interromper:
            break
