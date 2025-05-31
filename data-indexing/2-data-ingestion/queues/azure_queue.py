
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from .base import MessageQueueConnection, MessageHandler


class AzureServiceBusConnection(MessageQueueConnection):
    """Azure Service Bus implementation of the MessageQueueConnection abstract class."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, connection_string: str, queue_name: str):
        if not hasattr(self, '_initialized'):  # Ensure __init__ is only called once
            self.connection_string = connection_string
            self.queue_name = queue_name
            self._client = None
            self._sender = None
            self._initialized = True

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        if not self.is_connected():
            self._client = ServiceBusClient.from_connection_string(self.connection_string)
            self._sender = self._client.get_queue_sender(self.queue_name)

    def close(self):
        if self._sender:
            self._sender.close()
            self._sender = None
        if self._client:
            self._client.close()
            self._client = None

    def send_message(self, queue_name: str, message: str):
        if not self.is_connected():
            self.connect()
        service_bus_message = ServiceBusMessage(message)
        self._sender.send_messages(service_bus_message)
        print("Sent message to Azure Service Bus:", message)

    def is_connected(self) -> bool:
        return self._client is not None and self._sender is not None
    


class AzureServiceBusMessageHandler(MessageHandler):
    def send_message(self, queue_name: str, message: str):
        with self.connection:
            service_bus_message = ServiceBusMessage(message)
            self.connection._sender.send_messages(service_bus_message)