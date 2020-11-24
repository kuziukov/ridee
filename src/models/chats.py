from datetime import datetime

from bson import ObjectId
from umongo import (
    Document,
    fields
)
from extentions.mongo import instance
from .users import Users


@instance.register
class Chats(Document):
    _id = fields.ObjectIdField()
    name = fields.StringField(required=True)
    members = fields.ListField(fields.ReferenceField(Users), default=[])
    user = fields.ReferenceField(Users, required=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)

    class Meta:
        collection_name = "chats"

    async def list_members(self) -> list:
        return [await self.user.fetch() for user in self.members]

    async def get_user(self):
        return await self.user.fetch()

    @staticmethod
    async def is_user_in_chat(chat_id: str, user_id: str) -> bool:
        chat = await Chats.find_one({'_id': ObjectId(chat_id), 'members.': ObjectId(user_id)})
        return True if chat else False
