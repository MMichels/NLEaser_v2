from nleaser_models import connect_db
from nleaser_sources.logger import create_logger
from nleaser_workers.wordcloud_create import wordcloud_create_consumer


logger = create_logger("nleaser_worker_wordcloud_create")

if __name__ == '__main__':
    import time
    import logging
    from nleaser_sources.rabbit.consumer import RabbitConsumer

    while True:
        connect_db()
        pika_logger = logging.getLogger("pika")
        pika_logger.setLevel(logging.ERROR)

        try:
            logger.info("Conectando ao rabbitmq")
            consumer = RabbitConsumer("NLEaser.nleaser_worker_wordcloud_create")
            logger.info("Consumindo")
            consumer.consume(wordcloud_create_consumer, auto_ack=False, prefetch=1)

        except Exception as e:
            logger.error("Erro ao consumir mensagem", exc_info=True)
            time.sleep(5)