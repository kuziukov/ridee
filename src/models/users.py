from extentions.mongo import instance
from umongo import (
    Document,
    fields,
)


@instance.register
class Users(Document):
    _id = fields.ObjectIdField()
    name = fields.StringField()
    surname = fields.StringField()
    phone = fields.StringField(required=True)
    region_code = fields.StringField(required=True)
    blocked = fields.BooleanField(default=False)

    class Meta:
        collection_name = "users"
