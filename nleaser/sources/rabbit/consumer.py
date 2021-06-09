import threading

from nleaser.sources.rabbit import RabbitConector


class RabbitConsumer(RabbitConector):

    def consume(self, callback, auto_ack=True, prefetch=1, long_time_process=False):
        if self.channel is None or self.connection is None:
            self.connect()

        self.channel.basic_qos(prefetch_count=prefetch)

        if long_time_process:
            timer = threading.Timer(20, lambda: self.connection.process_data_events(30))
            timer.start()

            def long_time_process_callback(*args, **kwargs):
                result = callback(*args, **kwargs)
                timer.cancel()
                return result

            self.channel.basic_consume(
                queue=self.queue,
                auto_ack=auto_ack,
                on_message_callback=long_time_process_callback
            )

        else:
            self.channel.basic_consume(
                queue=self.queue,
                auto_ack=auto_ack,
                on_message_callback=callback
            )

        self.channel.start_consuming()
