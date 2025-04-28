from abc import ABC, abstractmethod

class BaseRetriever(ABC):
    
    @abstractmethod
    def gen(self, *args, **kwargs):
        pass
