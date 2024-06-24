
from . import ultrondb as db

fsub = db.force_sub


def fs_settings(chat_id: int):
    return _x if (_x := fsub.find_one({"chat_id": chat_id})) else None


def add_channel(chat_id: int, channel):
    fsub.update_one({"chat_id": chat_id}, {"$set": {"channel": channel}}, upsert=True)


def disapprove(chat_id: int):
    fsub.delete_one({"chat_id": chat_id})
