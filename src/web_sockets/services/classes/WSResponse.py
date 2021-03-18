from web_sockets.services.abstracts import AbstractEventResponse


class WSResponse:

    def __init__(self):
        pass

    @property
    def event_response(self) -> AbstractEventResponse:
        return self._eventResponse

    @event_response.setter
    def event_response(self, eventResponse: AbstractEventResponse) -> None:
        self._eventResponse = eventResponse

    async def make_response(self, event: dict) -> dict:
        response = await self._eventResponse.response(event)
        return response
