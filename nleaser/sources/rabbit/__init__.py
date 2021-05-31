import pika as pk

from queues import get_queue_config

from nleaser.config import RABBIT_HOST, RABBIT_PORT
from nleaser.models.config import ConfigModel


class RabbitConector:
    rabbit_host = RABBIT_HOST
    rabbit_port = RABBIT_PORT
    channel: pk.adapters.blocking_connection.BlockingChannel = None

    def __init__(self, queue_name):
        self.rabbit_user = ConfigModel.objects(name="RABBIT_USER").first().value
        self.rabbit_pass = ConfigModel.objects(name="RABBIT_PASS").first().value

        rabbit_queue = get_queue_config(queue_name)
        self.exchange = rabbit_queue["exchange"]
        self.routing_key = rabbit_queue["routing_key"]
        self.queue = rabbit_queue["queue"]

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