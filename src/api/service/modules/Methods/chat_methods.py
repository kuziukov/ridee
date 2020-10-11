from bson import ObjectId
from extentions.mongo import instance
from models.chats import (
    Chat,
    Member
)


class ChatMethods(object):

    @staticmethod
    async def create_chat(user_id: str, trip_id: str):
        chat = Chat()
        chat.name = 'Chat'
        chat.user_id = ObjectId(user_id)
        chat.trip_id = ObjectId(trip_id)

        result = await instance.db.chats.insert_one(chat.to_short_dict())
        return result

    @staticmethod
    async def execute_user_from_chat(chat_id: str, user_id: str):
        result = await instance.db.chats.update_one(
            {
                '_id': ObjectId(chat_id),
                'members': {
                    '$elemMatch': {
                        'user_id': ObjectId(user_id)
                    }
                }
            },
            {
                '$pull':
                    {
                        'members': {
                            'user_id': ObjectId(user_id)
                        }
                    }
            })
        return result

    @staticmethod
    async def invite_user_to_chat(chat_id: str, user_id: str):
        member = Member()
        member.user_id = ObjectId(user_id)

        result = await instance.db.chats.update_one(
            {
                '_id': ObjectId(chat_id),
                'members': {
                    '$not': {
                        '$elemMatch': {
                            'user_id': ObjectId(user_id)
                        }
                    }
                }
            },
            {
                '$addToSet':
                    {
                        'members': member.to_short_dict()
                    }
            })
        return result

    @staticmethod
    async def get_all_chats_by_id(user_id: str):
        chats = instance.db.chats.find({'members.user_id': ObjectId(user_id)})
        result = {
            'chats': [document async for document in chats]
        }
        return result

    @staticmethod
    async def get_chat_by_id(chat_id: str, user_id: str):
        chat = await instance.db.chats.find_one(
            {
                '_id': ObjectId(chat_id),
                'members': {
                    '$elemMatch': {
                        'user_id': ObjectId(user_id)
                    }
                }
            })
        return chat
