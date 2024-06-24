from platform import python_version as y

from pyrogram import __version__ as z
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import __version__ as o
from telethon import __version__ as s

from Ava import Jarvis as pbot

REPOIMG = "https://telegra.ph/file/94a4d5d7f7b2892e3bdbe.jpg"


@pbot.on_cmd("repo")
async def repo(_, message):
    await message.reply_photo(
        photo=REPOIMG,
        caption=f"""✨ **ʜᴇʏ {message.from_user.mention},**

**ᴏᴡɴᴇʀ  : [ᴏᴡɴᴇʀ](https://t.me/JARVIS_V2)**
**ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{y()}`
**ʟɪʙʀᴀʀʏ ᴠᴇʀꜱɪᴏɴ :** `{o}`
**ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{s}`
**ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ :** `{z}`
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "•ᴍᴜꜱɪᴄ•", url="https://github.com/doraemon890/ANNIE-X-MUSIC"
                    ),
                    InlineKeyboardButton(
                        "•ʀᴏʙᴏ•", url="https://github.com/doraemon890/AvaRobot"
                    ),
                ]
            ]
        ),
    )
