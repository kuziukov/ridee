from bson import ObjectId
from pymongo import ReturnDocument
from cores.rest_core import APIException, codes
from api.service.decorator import login_required
from cores.marshmallow_core import ApiSchema, fields
from api.resources.users.schemas import SerializationSchema


class DeserializationSchema(ApiSchema):

    name = fields.Str()
    surname = fields.Str()


class ProfileException(APIException):

    @property
    def message(self):
        return 'Username or surname is wrong. Please check the data.'

    code = codes.BAD_REQUEST


@login_required(skip_info=True)
async def UserPost(request):

    user = request.user
    data = DeserializationSchema().deserialize(await request.json())
    try:
        result = await request.app.db.users.find_one_and_update({'_id': ObjectId(user['_id'])},
                                                       {'$set': {'name': data['name'], 'surname': data['surname']}},
                                                        return_document=ReturnDocument.AFTER)
    except Exception as e:
        raise ProfileException()
    return SerializationSchema().serialize(result)
