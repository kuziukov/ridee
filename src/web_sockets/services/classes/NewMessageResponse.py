from web_sockets.services.abstracts import (
    AbstractEventResponse
)


class NewMessageResponse(AbstractEventResponse):

    async def response(self, event: dict) -> dict:
        return event
