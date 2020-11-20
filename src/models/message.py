import datetime

import pymongo
from bson import ObjectId
from umongo import (
    Document,
    fields
)
from extentions.mongo import instance
from models import (
    Chats,
    Users
)


@instance.register
class Messages(Document):
    _id = fields.ObjectIdField()
    random_id = fields.StringField(required=True)
    message = fields.StringField(required=True)
    chat = fields.ReferenceField(Chats, required=True)
    user = fields.ReferenceField(Users, required=True)
    is_deleted = fields.BooleanField(default=False)
    created_at = fields.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        collection_name = "messages"

    @staticmethod
    async def last_message(chat_id: ObjectId) -> dict:
        last_message = Messages.find({'chat': chat_id}).sort([('created_at', pymongo.DESCENDING)])
        last_message = await last_message.to_list(1)
        last_message = last_message[0] if last_message else None
        return {
            '_id': last_message._id,
            'message': last_message.message,
            'user': await last_message.user.fetch(),
            'chat': await last_message.chat.fetch(),
            'created_at': last_message.created_at
        } if last_message else None

    @staticmethod
    async def range_messages(query, count=20, skip=0) -> list:
        response = []
        messages = Messages.find(query).sort([('created_at', pymongo.DESCENDING)]).skip(skip)
        messages = await messages.to_list(count)
        for message in messages:
            response.append({
                '_id': message._id,
                'user': await message.user.fetch(),
                'message': message.message,
                'created_at': message.created_at
            })
        return response