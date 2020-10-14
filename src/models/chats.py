from datetime import datetime
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
    created_at = fields.DateTimeField(default=datetime.utcnow())

    class Meta:
        collection_name = "chats"
