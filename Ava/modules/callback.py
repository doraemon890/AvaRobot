from pyrogram.types import CallbackQuery
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackQueryHandler, Dispatcher

from Ava import BOT_NAME, OWNER_ID, SUPPORT_CHAT
from Ava import Jarvis as pbot
from Ava import dispatcher

@pbot.on_callback_query()
async def close(client, cb: CallbackQuery):
    if cb.data == "close2":
        await cb.answer()
        await cb.message.delete()


# CALLBACKS

def Jarvis_about_callback(update, context):
    query = update.callback_query
    if query.data == "Jarvis_":
        query.message.edit_caption(
            caption=f"๏ ɪ'ᴍ {BOT_NAME}, ᴀ ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ʙᴜɪʟᴛ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇᴀsɪʟʏ."
                    "\n๏  I scan ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs."
                    "\n๏  I ᴄᴀɴ ɢʀᴇᴇᴛ ᴜsᴇʀs ᴡɪᴛʜ ᴄᴜsᴛᴏᴍɪsᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇs ᴀɴᴅ ᴇᴠᴇɴ sᴇᴛ ᴀ ɢʀᴏᴜᴘ's ʀᴜʟᴇs."
                    "\n๏  I ʜᴀᴠᴇ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴛɪ-ғʟᴏᴏᴅ sʏsᴛᴇᴍ."
                    "\n๏  I ᴄᴀɴ ᴡᴀʀɴ ᴜsᴇʀs ᴜɴᴛɪʟ ᴛʜᴇʏ ʀᴇᴀᴄʜ ᴍᴀx ᴡᴀʀɴs, ᴡɪᴛʜ ᴇᴀᴄʜ ᴘʀᴇᴅᴇғɪɴᴇᴅ ᴀᴄᴛɪᴏɴs sᴜᴄʜ ᴀs ʙᴀɴ, ᴍᴜᴛᴇ, ᴋɪᴄᴋ, ᴇᴛᴄ."
                    "\n๏  I ʜᴀᴠᴇ ᴀ ɴᴏᴛᴇ-ᴋᴇᴇᴘɪɴɢ sʏsᴛᴇᴍ, ʙʟᴀᴄᴋʟɪsᴛs, ᴀɴᴅ ᴇᴠᴇɴ ᴘʀᴇᴅᴇᴛᴇʀᴍɪɴᴇᴅ ʀᴇᴘʟɪᴇs ᴏɴ ᴄᴇʀᴛᴀɪɴ ᴋᴇʏᴡᴏʀᴅs."
                    "\n๏  I ᴄʜᴇᴄᴋ ғᴏʀ ᴀᴅᴍɪɴs ᴘᴇʀᴍɪssɪᴏɴs ʙᴇғᴏʀᴇ ᴇxᴇᴄᴜᴛɪɴɢ ᴀɴʏ ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ᴍᴏʀᴇ sᴛᴜғғ."
                    "\n\nᴀᴠᴀ ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ GNU ɢᴇɴᴇʀᴀʟ ᴘᴜʙʟɪᴄ ʟɪᴄᴇɴsᴇ v3.0."
                    "\n\n*ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ʙᴀsɪᴄ ʜᴇʟᴘ ғᴏʀ ᴀᴠᴀʀᴏʙᴏᴛ*.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ɴᴏᴛᴇs", callback_data="Jarvis_notes"),
                    ],
                    [
                        InlineKeyboardButton(
                            text="sᴜᴘᴘᴏʀᴛ", callback_data="Jarvis_support"
                        ),
                        InlineKeyboardButton(
                            text="sᴏᴜʀᴄᴇ",
                            callback_data="source_",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ɢᴏ ʙᴀᴄᴋ", callback_data="start_back"
                        ),
                    ],
                ]
            ),
        )

    elif query.data == "Jarvis_notes":
        query.message.edit_caption(
            caption=f"<b>๏ sᴇᴛᴛɪɴɢ ᴜᴘ ɴᴏᴛᴇs</b>"
                    f"\n\n➻ʏᴏᴜ ᴄᴀɴ sᴀᴠᴇ ᴍᴇssᴀɢᴇ/ᴍᴇᴅɪᴀ/ᴀᴜᴅɪᴏ ᴏʀ ᴀɴʏᴛʜɪɴɢ ᴀs ɴᴏᴛᴇs"
                    f"\n➻ᴛᴏ ɢᴇᴛ ᴀ ɴᴏᴛᴇ sɪᴍᴘʟʏ ᴜsᴇ # ᴀᴛ ᴛʜᴇ ʙᴇɢɪɴɴɪɴɢ ᴏғ ᴀ ᴡᴏʀᴅ"
                    f"\n➻nʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ sᴇᴛ ʙᴜᴛᴛᴏɴs ғᴏʀ ɴᴏᴛᴇs ᴀɴᴅ ғɪʟᴛᴇʀs ʀᴇғᴇʀ ʜᴇʟᴘ ᴍᴇɴᴜ",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ɢᴏ ʙᴀᴄᴋ", callback_data="Jarvis_")]]
            ),
        )
    elif query.data == "Jarvis_support":
        query.message.edit_caption(
            caption=f"*๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ʜᴇʟᴩ ᴀɴᴅ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ*"
                    "\n\n➲ ɪғ ʏᴏᴜ ғᴏᴜɴᴅ ᴀɴʏ ʙᴜɢ ɪɴ [ᴀᴠᴀʀᴏʙᴏᴛ](https://t.me/Ava_The_Robot) ᴏʀ ɪғ ʏᴏᴜ ᴡᴀɴɴᴀ ɢɪᴠᴇ ғᴇᴇᴅʙᴀᴄᴋ ᴀʙᴏᴜᴛ ᴛʜᴇ [ᴀᴠᴀʀᴏʙᴏᴛ](https://t.me/Ava_The_Robot), ᴩʟᴇᴀsᴇ ʀᴇᴩᴏʀᴛ ɪᴛ ᴀᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="sᴜᴘᴘᴏʀᴛ", url=f"t.me/{SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            text="ᴜᴘᴅᴀᴛᴇs", url="https://t.me/JARVIS_V_SUPPORT"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴅᴇᴠᴇʟᴏᴩᴇʀ", url=f"tg://user?id={OWNER_ID}"
                        ),
                        InlineKeyboardButton(
                            text="ɢɪᴛʜᴜʙ", url="https://github.com/doraemon890",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="ɢᴏ ʙᴀᴄᴋ", callback_data="Jarvis_"),
                    ],
                ]
            ),
        )


def Source_about_callback(update, context):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_caption(
            caption=f"""
**ʜᴇʏ,
ᴛʜɪs ɪs {BOT_NAME},
ᴀɴ ᴏᴩᴇɴ sᴏᴜʀᴄᴇ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴩ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ.**

ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ ᴛʜᴇ ʜᴇʟᴩ ᴏғ: [ᴛᴇʟᴇᴛʜᴏɴ](https://github.com/LonamiWebs/Telethon)
[ᴩʏʀᴏɢʀᴀᴍ](https://github.com/pyrogram/pyrogram)
[ᴩʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ](https://github.com/python-telegram-bot/python-telegram-bot)
ᴀɴᴅ ᴜsɪɴɢ [sǫʟᴀʟᴄʜᴇᴍʏ](https://www.sqlalchemy.org) ᴀɴᴅ [ᴍᴏɴɢᴏ](https://cloud.mongodb.com) ᴀs ᴅᴀᴛᴀʙᴀsᴇs.

*ʜᴇʀᴇ ɪs ᴍʏ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ:* [{BOT_NAME}](https://github.com/doraemon890/AvaRobot)

{BOT_NAME} ɪs ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ [ᴍɪᴛ ʟɪᴄᴇɴsᴇ](https://github.com/doraemon890/AvaRobot/blob/master/LICENSE).
© 2022 - 2023 [sᴜᴘᴘᴏʀᴛ](https://t.me/{SUPPORT_CHAT}) ᴄʜᴀᴛ, ᴀʟʟ ʀɪɢʜᴛs ʀᴇsᴇʀᴠᴇᴅ.
""",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ꜱᴏᴜʀᴄᴇ", url="https://github.com/doraemon890/AvaRobot"),
                    ],
                    [
                        InlineKeyboardButton(text="ɢᴏ ʙᴀᴄᴋ", callback_data="Jarvis_"),
                    ],
                ]
            ),
        )


about_callback_handler = CallbackQueryHandler(
    Jarvis_about_callback, pattern=r"Jarvis_", run_async=True
)

source_callback_handler = CallbackQueryHandler(
    Source_about_callback, pattern=r"source_", run_async=True
)


dispatcher.add_handler(about_callback_handler)
dispatcher.add_handler(source_callback_handler)
