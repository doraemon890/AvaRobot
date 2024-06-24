from Ava.modules.no_sql import Jarvisdb

afkdb = Jarvisdb.afk


async def is_afk(user_id: int) -> bool:
    user = await afkdb.find_one({"user_id": user_id})
    return (True, user["reason"]) if user else (False, {})


async def add_afk(user_id: int, mode):
    await afkdb.update_one(
        {"user_id": user_id}, {"$set": {"reason": mode}}, upsert=True
    )


async def remove_afk(user_id: int):
    user = await afkdb.find_one({"user_id": user_id})
    if user:
        return await afkdb.delete_one({"user_id": user_id})


async def get_afk_users() -> list:
    users = afkdb.find({"user_id": {"$gt": 0}})
    return list(await users.to_list(length=1000000000)) if users else []
