from datetime import datetime

from extentions.mongo import instance
from umongo import (
    Document,
    fields,
    EmbeddedDocument
)


@instance.register
class LastCoordinates(EmbeddedDocument):

    lat = fields.FloatField(required=True)
    long = fields.FloatField(required=True)


@instance.register
class Users(Document):
    _id = fields.ObjectIdField()
    name = fields.StringField()
    surname = fields.StringField()
    phone = fields.StringField(required=True)
    region_code = fields.StringField(required=True)
    blocked = fields.BooleanField(default=False)
    last_coord = fields.EmbeddedField(LastCoordinates)
    created_at = fields.DateTimeField(default=datetime.utcnow)

    class Meta:
        collection_name = "users"
