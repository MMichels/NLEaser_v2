import pika as pk

from nleaser.config import RABBIT_HOST
from nleaser.models.config import ConfigModel
from nleaser.models.config.rabbit_queues import RabbitQueueConfigModel


class RabbitConector():
    rabbit_host = RABBIT_HOST
    channel: pk.adapters.blocking_connection.BlockingChannel = None

    def __init__(self, queue_name):
        self.rabbit_port = ConfigModel.objects(name="RABBIT_PORT").first().value
        self.rabbit_user = ConfigModel.objects(name="RABBIT_USER").first().value
        self.rabbit_pass = ConfigModel.objects(name="RABBIT_PASS").first().value

        rabbit_queue: RabbitQueueConfigModel = RabbitQueueConfigModel.objects(name=queue_name).first()
        self.exchange = rabbit_queue.value.exchange
        self.routing_key = rabbit_queue.value.routing_key
        self.queue = rabbit_queue.value.queue

    def connect(self):
        creds = pk.PlainCredentials(
            username=self.rabbit_user,
            password=self.rabbit_pass
        )
        params = pk.ConnectionParameters(
            host=self.rabbit_host,
            port=self.rabbit_port,
            credentials=creds,
            heartbeat=0
        )
        conn = pk.BlockingConnection(parameters=params)

        channel = conn.channel()
        channel.exchange_declare(
            exchange=self.exchange,
            durable=True
        )
        channel.queue_declare(
            queue=self.queue,
            durable=True
        )
        channel.queue_bind(
            exchange=self.exchange,
            queue=self.queue,
            routing_key=self.routing_key
        )

        self.channel = channel

        return channel
