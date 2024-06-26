import threading

from sqlalchemy import Column, String, UnicodeText

from Ava.modules.sql import BASE, SESSION


class ChatLangs(BASE):
    __tablename__ = "chatlangs"
    chat_id = Column(String(14), primary_key=True)  # ensure chat_id is a string
    language = Column(UnicodeText)

    def __init__(self, chat_id, language):
        self.chat_id = str(chat_id)  # ensure chat_id is a string
        self.language = language

    def __repr__(self):
        return f"Language {self.language} chat {self.chat_id}"


CHAT_LANG = {}
LANG_LOCK = threading.RLock()
ChatLangs.__table__.create(checkfirst=True)


def set_lang(chat_id: str, lang: str) -> None:
    with LANG_LOCK:
        chat_id = str(chat_id)  # ensure chat_id is a string
        if curr := SESSION.query(ChatLangs).get(chat_id):
            curr.language = lang
        else:
            curr = ChatLangs(chat_id, lang)
            SESSION.add(curr)
            SESSION.flush()
        CHAT_LANG[chat_id] = lang
        SESSION.commit()


def get_chat_lang(chat_id: str) -> str:
    chat_id = str(chat_id)  # ensure chat_id is a string
    lang = CHAT_LANG.get(chat_id)
    if lang is None:
        lang = "en"
    return lang


def __load_chat_language() -> None:
    global CHAT_LANG
    try:
        allchats = SESSION.query(ChatLangs).all()
        CHAT_LANG = {str(x.chat_id): x.language for x in allchats}  # ensure all chat_ids are strings
    finally:
        SESSION.close()


__load_chat_language()
