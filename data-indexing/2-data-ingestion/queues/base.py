from abc import ABC, abstractmethod

class MessageQueueConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass

class MessageHandler(ABC):
    def __init__(self, connection: MessageQueueConnection):
        self.connection = connection

    @abstractmethod
    def send_message(self, queue_name: str, message: str):
        pass