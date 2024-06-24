from emoji import UNICODE_EMOJI
from telegram import Message
from telegram.ext import MessageFilter

from Ava import DEMONS, DEV_USERS


class CustomFilters:
    class _Supporters(MessageFilter):
        def filter(self, message: Message):
            return bool(message.from_user and message.from_user.id in DEMONS)

    support_filter = _Supporters()

    class _Sudoers(MessageFilter):
        def filter(self, message: Message):
            return bool(message.from_user and message.from_user.id in DEV_USERS)

    dev_filter = _Sudoers()

    class _MimeType(MessageFilter):
        def __init__(self, mimetype):
            self.mime_type = mimetype
            self.name = f"CustomFilters.mime_type({self.mime_type})"

        def filter(self, message: Message):
            return bool(
                message.document and message.document.mime_type == self.mime_type
            )

    mime_type = _MimeType

    class _HasText(MessageFilter):
        def filter(self, message: Message):
            return bool(
                message.text
                or message.sticker
                or message.photo
                or message.document
                or message.video
            )

    has_text = _HasText()

    class _HasEmoji(MessageFilter):
        def filter(self, message: Message):
            text = message.text or ""
            for emoji in UNICODE_EMOJI:
                for letter in text:
                    if letter == emoji:
                        return True
            return False

    has_emoji = _HasEmoji()

    class _IsEmoji(MessageFilter):
        def filter(self, message: Message):
            if message.text and len(message.text) == 1:
                for emoji in UNICODE_EMOJI:
                    for letter in message.text:
                        if letter == emoji:
                            return True
            return False

    is_emoji = _IsEmoji()

    class _IsAnonChannel(MessageFilter):
        def filter(self, message: Message):
            return bool(message.from_user and message.from_user.id == 136817688)

    is_anon_channel = _IsAnonChannel()
