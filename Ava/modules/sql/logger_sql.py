import threading

from sqlalchemy import Boolean, Column, String

from Ava.modules.sql import BASE, SESSION


class LoggerSettings(BASE):
    __tablename__ = "chat_log_settings"
    chat_id = Column(String(14), primary_key=True)
    setting = Column(Boolean, default=False, nullable=False)

    def __init__(self, chat_id, disabled):
        self.chat_id = str(chat_id)
        self.setting = disabled

    def __repr__(self):
        return f"<Chat log setting {self.chat_id} ({self.setting})>"


LoggerSettings.__table__.create(checkfirst=True)

LOG_SETTING_LOCK = threading.RLock()


def enable_chat_log(chat_id):
    with LOG_SETTING_LOCK:
        chat = SESSION.query(LoggerSettings).get(str(chat_id)) or LoggerSettings(chat_id, True)
        chat.setting = True
        SESSION.add(chat)
        SESSION.commit()


def disable_chat_log(chat_id):
    with LOG_SETTING_LOCK:
        chat = SESSION.query(LoggerSettings).get(str(chat_id)) or LoggerSettings(chat_id, False)

        chat.setting = False
        SESSION.add(chat)
        SESSION.commit()


def does_chat_log(chat_id):
    with LOG_SETTING_LOCK:
        d = SESSION.query(LoggerSettings).get(str(chat_id))
        return d.setting if d else False


def migrate_chat(old_chat_id, new_chat_id):
    with LOG_SETTING_LOCK:
        if chat := SESSION.query(LoggerSettings).get(str(old_chat_id)):
            chat.chat_id = new_chat_id
            SESSION.add(chat)

        SESSION.commit()
