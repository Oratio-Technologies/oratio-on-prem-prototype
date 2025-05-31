import pika
from .base import MessageQueueConnection, MessageHandler

class RabbitMQConnection(MessageQueueConnection):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, port, username, password, virtual_host="/"):
        if not hasattr(self, '_initialized'):
            self.host = host
            self.port = port
            self.username = username
            self.password = password
            self.virtual_host = "/"
            self._connection = None
            self._initialized = True
            
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
            
    def connect(self):
        if not self.is_connected():
            credentials = pika.PlainCredentials(self.username, self.password)
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    virtual_host=self.virtual_host,
                    credentials=credentials,
                )
            )

    def close(self):
        if self.is_connected():
            self._connection.close()
            self._connection = None

    def is_connected(self) -> bool:
        return self._connection is not None and self._connection.is_open

    def get_channel(self):
        if self.is_connected():
            return self._connection.channel()

class RabbitMQMessageHandler(MessageHandler):
    def send_message(self, queue_name: str, message: str):
        try:
            with self.connection:
                channel = self.connection.get_channel()
                channel.queue_declare(queue=queue_name, durable=True)
                channel.confirm_delivery()
                channel.basic_publish(
                    exchange="",
                    routing_key=queue_name,
                    body=message,
                    properties=pika.BasicProperties(delivery_mode=2),
                )
        except pika.exceptions.UnroutableError:
            print("Message could not be routed")
        except Exception as e:
            print(f"Error publishing to RabbitMQ: {e}")