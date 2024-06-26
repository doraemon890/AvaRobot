
from typing import Dict, Union

from . import ultrondb as db

couplesdb = db.couple
karmadb = db.karma


async def _get_lovers(chat_id: int):
    lovers = couplesdb.find_one({"chat_id": chat_id})
    lovers = lovers["couple"] if lovers else {}
    return lovers


async def get_couple(chat_id: int, date: str):
    lovers = await _get_lovers(chat_id)
    return lovers[date] if date in lovers else False


async def save_couple(chat_id: int, date: str, couple: dict):
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    couplesdb.update_one(
        {"chat_id": chat_id}, {"$set": {"couple": lovers}}, upsert=True
    )


async def get_karmas_count() -> dict:
    chats = karmadb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return {}
    chats_count = 0
    karmas_count = 0
    for chat in await chats.to_list(length=1000000):
        for i in chat["karma"]:
            karma_ = chat["karma"][i]["karma"]
            if karma_ > 0:
                karmas_count += karma_
        chats_count += 1
    return {"chats_count": chats_count, "karmas_count": karmas_count}


async def user_global_karma(user_id) -> int:
    chats = karmadb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return 0
    total_karma = 0
    for chat in await chats.to_list(length=1000000):
        karma = await get_karma(chat["chat_id"], await int_to_alpha(user_id))
        if karma and (int(karma["karma"]) > 0):
            total_karma += int(karma["karma"])
    return total_karma


async def get_karmas(chat_id: int) -> Dict[str, int]:
    karma = karmadb.find_one({"chat_id": chat_id})
    return karma["karma"] if karma else {}


async def get_karma(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    karmas = await get_karmas(chat_id)
    if name in karmas:
        return karmas[name]


async def update_karma(chat_id: int, name: str, karma: dict):
    name = name.lower().strip()
    karmas = await get_karmas(chat_id)
    karmas[name] = karma
    karmadb.update_one({"chat_id": chat_id}, {"$set": {"karma": karmas}}, upsert=True)


async def is_karma_on(chat_id: int) -> bool:
    chat = karmadb.find_one({"chat_id_toggle": chat_id})
    return not chat


async def karma_on(chat_id: int):
    is_karma = await is_karma_on(chat_id)
    if is_karma:
        return
    return karmadb.delete_one({"chat_id_toggle": chat_id})


async def karma_off(chat_id: int):
    is_karma = await is_karma_on(chat_id)
    if not is_karma:
        return
    return karmadb.insert_one({"chat_id_toggle": chat_id})


async def int_to_alpha(user_id: int) -> str:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = str(user_id)
    return "".join(alphabet[int(i)] for i in user_id)


async def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for i in user_id_alphabet:
        index = alphabet.index(i)
        user_id += str(index)
    return int(user_id)
