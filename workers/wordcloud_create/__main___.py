from nleaser.models import connect_db
from nleaser.sources.logger import create_logger
from workers.wordcloud_create import wordcloud_create_consumer


logger = create_logger("_wordcloud_create")

if __name__ == '__main__':
    import time
    import logging
    from nleaser.sources.rabbit.consumer import RabbitConsumer

    while True:
        connect_db()
        pika_logger = logging.getLogger("pika")
        pika_logger.setLevel(logging.ERROR)

        try:
            logger.info("Conectando ao rabbitmq")
            consumer = RabbitConsumer("NLEaser._wordcloud_create")
            logger.info("Consumindo")
            consumer.consume(wordcloud_create_consumer, auto_ack=False, prefetch=1)

        except Exception as e:
            logger.error("Erro ao consumir mensagem", exc_info=True)
            time.sleep(5)