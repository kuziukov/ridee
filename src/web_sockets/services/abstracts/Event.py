from abc import (
    ABC,
    abstractmethod
)


class AbstractEventResponse(ABC):

    def __init__(self):
        pass

    @abstractmethod
    async def response(self, event: dict) -> dict:
        pass
