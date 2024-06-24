from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pymongo import MongoClient, collection

from Ava import DB_NAME
from Ava import MONGO_URI as MONGO_DB_URI

mongo = MongoCli(MONGO_DB_URI)
Jarvisdb = mongo.AvaRobot_

try:
    client = MongoClient(MONGO_DB_URI)
except PyMongoError:
    exiter(1)
main_db = client[DB_NAME]


ultrondb = main_db


def get_collection(name: str) -> collection:
    """ɢᴇᴛ ᴛʜᴇ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ."""
    return ultrondb[name]


class MongoDB:
    """Class for interacting with Bot database."""

    def __init__(self, collection) -> None:
        self.collection = ultrondb[collection]

    # Insert one entry into collection
    def insert_one(self, document):
        result = self.collection.insert_one(document)
        return repr(result.inserted_id)

    # Find one entry from collection
    def find_one(self, query):
        return result if (result := self.collection.find_one(query)) else False

    # Find entries from collection
    def find_all(self, query=None):
        if query is None:
            query = {}
        return list(self.collection.find(query))

    # Count entries from collection
    def count(self, query=None):
        if query is None:
            query = {}
        return self.collection.count_documents(query)

    # Delete entry/entries from collection
    def delete_one(self, query):
        self.collection.delete_many(query)
        return self.collection.count_documents({})

    # Replace one entry in collection
    def replace(self, query, new_data):
        old = self.collection.find_one(query)
        _id = old["_id"]
        self.collection.replace_one({"_id": _id}, new_data)
        new = self.collection.find_one({"_id": _id})
        return old, new

    # Update one entry from collection
    def update(self, query, update):
        result = self.collection.update_one(query, {"$set": update})
        new_document = self.collection.find_one(query)
        return result.modified_count, new_document

    @staticmethod
    def close():
        return client.close()


def __connect_first():
    _ = MongoDB("test")


__connect_first()
