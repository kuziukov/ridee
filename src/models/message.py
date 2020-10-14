from datetime import datetime
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
    created_at = fields.DateTimeField(default=datetime.utcnow())

    class Meta:
        collection_name = "messages"
