import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from bson import ObjectId


@dataclass
class Member:
    user_id: ObjectId = None
    created_at: datetime = datetime.utcnow()

    def to_short_dict(self):
        result = asdict(self)
        return result


@dataclass
class Chat:
    _id: str = None
    name: str = None
    members: list = field(default_factory=list)
    user_id: ObjectId = None
    trip_id: ObjectId = None
    created_at: datetime = datetime.utcnow()

    def to_json(self):
        return json.dumps(self.__dict__, default=lambda x: x.__dict__, indent=4)

    def to_short_dict(self):
        result = asdict(self)
        return result
