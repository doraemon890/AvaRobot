import threading

from sqlalchemy import Boolean, Column
from sqlalchemy.sql.sqltypes import String

from Ava.modules.sql import BASE, SESSION


class AntiLinkedChannelSettings(BASE):
    __tablename__ = "anti_linked_channel_settings"

    chat_id = Column(String(14), primary_key=True)
    setting = Column(Boolean, default=False, nullable=False)

    def __init__(self, chat_id: int, disabled: bool):
        self.chat_id = str(chat_id)
        self.setting = disabled

    def __repr__(self):
        return f"<Antilinked setting {self.chat_id} ({self.setting})>"


class AntiPinChannelSettings(BASE):
    __tablename__ = "anti_pin_channel_settings"

    chat_id = Column(String(14), primary_key=True)
    setting = Column(Boolean, default=False, nullable=False)

    def __init__(self, chat_id: int, disabled: bool):
        self.chat_id = str(chat_id)
        self.setting = disabled

    def __repr__(self):
        return f"<Antipin setting {self.chat_id} ({self.setting})>"


AntiLinkedChannelSettings.__table__.create(checkfirst=True)
ANTI_LINKED_CHANNEL_SETTING_LOCK = threading.RLock()

AntiPinChannelSettings.__table__.create(checkfirst=True)
ANTI_PIN_CHANNEL_SETTING_LOCK = threading.RLock()


def enable(chat_id: int):
    with ANTI_LINKED_CHANNEL_SETTING_LOCK:
        chat = SESSION.query(AntiLinkedChannelSettings).get(str(chat_id)) or AntiLinkedChannelSettings(chat_id, True)

        chat.setting = True
        SESSION.add(chat)
        SESSION.commit()


def enable_pin(chat_id: int):
    with ANTI_PIN_CHANNEL_SETTING_LOCK:
        chat = SESSION.query(AntiPinChannelSettings).get(str(chat_id)) or AntiPinChannelSettings(chat_id, True)

        chat.setting = True
        SESSION.add(chat)
        SESSION.commit()


def disable_linked(chat_id: int):
    with ANTI_LINKED_CHANNEL_SETTING_LOCK:
        chat = SESSION.query(AntiLinkedChannelSettings).get(str(chat_id)) or AntiLinkedChannelSettings(chat_id, False)

        chat.setting = False
        SESSION.add(chat)
        SESSION.commit()


def disable_pin(chat_id: int):
    with ANTI_PIN_CHANNEL_SETTING_LOCK:
        chat = SESSION.query(AntiPinChannelSettings).get(str(chat_id)) or AntiPinChannelSettings(chat_id, False)

        chat.setting = False
        SESSION.add(chat)
        SESSION.commit()


def status_linked(chat_id: int) -> bool:
    with ANTI_LINKED_CHANNEL_SETTING_LOCK:
        d = SESSION.query(AntiLinkedChannelSettings).get(str(chat_id))
        return d.setting if d else False


def status_pin(chat_id: int) -> bool:
    with ANTI_PIN_CHANNEL_SETTING_LOCK:
        d = SESSION.query(AntiPinChannelSettings).get(str(chat_id))
        return d.setting if d else False


def migrate_chat(old_chat_id, new_chat_id):
    with ANTI_LINKED_CHANNEL_SETTING_LOCK:
        if chat := SESSION.query(AntiLinkedChannelSettings).get(
            str(old_chat_id)
        ):
            chat.chat_id = new_chat_id
            SESSION.add(chat)

        SESSION.commit()
    with ANTI_PIN_CHANNEL_SETTING_LOCK:
        if chat := SESSION.query(AntiPinChannelSettings).get(str(old_chat_id)):
            chat.chat_id = new_chat_id
            SESSION.add(chat)

        SESSION.commit()
