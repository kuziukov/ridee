from models.message import Message
from extentions.mongo import instance


class MessageMethods(object):

    @staticmethod
    async def message(message: Message):
        result = await instance.db.messages.insert_one(message.to_short_dict())
        return result

    @staticmethod
    async def delete(message_id: str):
        pass


