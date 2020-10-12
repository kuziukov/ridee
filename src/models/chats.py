from datetime import datetime
from umongo import Document, fields
from extentions.mongo import instance


@instance.register
class Chats(Document):
    _id = fields.ObjectIdField()
    name = fields.StringField(required=True)
    members = fields.ListField(fields.ReferenceField("Users"))
    user = fields.ReferenceField("Users")
    created_at = fields.DateTimeField(default=datetime.utcnow())

    class Meta:
        collection_name = "chats"
