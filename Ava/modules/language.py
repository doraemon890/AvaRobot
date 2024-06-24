import itertools
from collections.abc import Iterable
from typing import Generator, List, Union

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

import Ava.modules.sql.language_sql as sql
from Ava.langs import get_language, get_languages, get_string
from Ava.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from Ava.modules.helper_funcs.decorators import Avacallback, Avacmd


def paginate(iterable: Iterable, page_size: int) -> Generator[List, None, None]:
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (
            itertools.islice(i1, page_size, None),
            list(itertools.islice(i2, page_size)),
        )
        if not page:
            break
        yield page


def gs(chat_id: Union[int, str], string: str) -> str:
    try:
        lang = sql.get_chat_lang(chat_id)
        return get_string(lang, string)
    except Exception:
        return "ᴍᴇ ɴᴏᴡ ʙᴜsʏ ᴡʜᴇɴ ғʀᴇᴇ ᴀᴅᴅ ᴛʜɪs "


@Avacmd(command="language")
@user_admin
def set_lang(update: Update, _) -> None:
    chat = update.effective_chat
    msg = update.effective_message

    msg_text = gs(chat.id, "curr_chat_lang").format(
        get_language(sql.get_chat_lang(chat.id))[:-3]
    )

    keyb = [
        InlineKeyboardButton(
            text=name,
            callback_data=f"setLang_{code}",
        )
        for code, name in get_languages().items()
    ]
    keyb = list(paginate(keyb, 2))
    msg.reply_text(msg_text, reply_markup=InlineKeyboardMarkup(keyb))


@Avacallback(pattern=r"setLang_")
@user_admin_no_reply
def lang_button(update: Update, _) -> None:
    query = update.callback_query
    chat = update.effective_chat

    query.answer()
    lang = query.data.split("_")[1]
    sql.set_lang(chat.id, lang)

    query.message.edit_text(
        gs(chat.id, "set_chat_lang").format(get_language(lang)[:-3])
    )
