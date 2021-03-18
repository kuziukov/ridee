from abc import (
    ABC,
    abstractmethod
)

from web_sockets.services.abstracts import (
    Subscriber
)


class AbstractPublisher(ABC):

    @abstractmethod
    def subscribe(self, subscriber: Subscriber) -> None:
        pass

    @abstractmethod
    def unsibscribe(self, subscriber: Subscriber) -> None:
        pass

    @abstractmethod
    async def notifySubscribers(self, message: dict) -> None:
        pass

    @abstractmethod
    async def broadcast(self):
        pass
