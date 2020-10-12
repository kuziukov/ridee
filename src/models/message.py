from dataclasses import (
    dataclass,
    asdict,
)
from datetime import datetime
from bson import ObjectId


@dataclass
class Message:
    _id: str = None
    random_id: str = None
    message: str = None
    chat_id: ObjectId = None
    user_id: ObjectId = None
    is_deleted: bool = False
    created_at: datetime = datetime.utcnow()

    def to_short_dict(self):
        result = asdict(self)
        return result
