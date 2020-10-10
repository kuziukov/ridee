from datetime import datetime

from bson import ObjectId
from extentions.mongo import instance


class Chats(object):

    @staticmethod
    async def message_to_chat(chat_id: str, data: dict):
        pass

    @staticmethod
    async def create_chat(user_id: str, trip_id: str):
        chat = {
            'name': 'Chat',
            'members': [],
            'user_id': ObjectId(user_id),
            'created_at': datetime.now()
        }
        result = await instance.db.chats.insert_one(chat)
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

    """
        if result.modified_count == 0:
            raise ChatsInvitationException()
    """
    @staticmethod
    async def invite_user_to_chat(chat_id: str, user_id: str):
        user = {
            'user_id': ObjectId(user_id),
            'created_at': datetime.now()
        }
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
                        'members': user
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
