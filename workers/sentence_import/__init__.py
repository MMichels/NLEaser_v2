from sources.logger import create_logger

logger = create_logger(__package__)


def sentence_preprocessor_consumer(ch, method, properties, body):
    logger.info("Recebido: ", extra={"received_args": body})

    ch.basic_ack(delivery_tag=method.delivery_tag)

    return True


if __name__ == '__main__':
    import time
    from sources.rabbit.consumer import RabbitConsumer

    while True:
        try:
            logger.info("Conectando ao rabbitmq")
            consumer = RabbitConsumer("NLEaser.sentence_import")
            logger.info("Consumindo")
            consumer.consume(sentence_preprocessor_consumer, auto_ack=False)

        except Exception as e:
            logger.error("Erro ao consumir mensagem", exc_info=True)
            time.sleep(5)
