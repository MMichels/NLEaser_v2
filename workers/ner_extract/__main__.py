from nleaser.models import connect_db
from nleaser.sources.logger import create_logger
from nleaser.sources.rabbit.consumer import RabbitConsumer
from workers.ner_extract import ner_resume_create_consumer

logger = create_logger("ner_resume_create")


if __name__ == '__main__':
    import logging
    import time

    while True:
        connect_db()
        pika_logger = logging.getLogger("pika")
        pika_logger.setLevel(logging.ERROR)

        try:
            logger.info("Conctando ao RabbitMQ")
            consumer = RabbitConsumer("NLEaser.ner_resume_create")
            logger.info("Consumindo")
            consumer.consume(ner_resume_create_consumer, auto_ack=False, prefetch=1, long_time_process=True)
        except Exception as e:
            logger.error("Erro ao consumir mensagem", exc_info=True)
            time.sleep(5)