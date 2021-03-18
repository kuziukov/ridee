from abc import (
    ABC,
    abstractmethod
)
from web_sockets.services.abstracts import (
    Publisher
)


class Subscriber(ABC):

    @abstractmethod
    async def update(self, publisher: Publisher) -> None:
        pass
