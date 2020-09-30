from bson import ObjectId
from typing import Dict
from cores.rest_core import APIException, codes
from extentions.mongo import instance


class UserNotFoundException(APIException):

    @property
    def message(self):
        return 'User have not found, please check your data.'

    code = codes.BAD_REQUEST


class Users(object):

    @staticmethod
    async def get_user_by_id(user_id) -> Dict:
        user = await instance.db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            raise UserNotFoundException()
        return user

