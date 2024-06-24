import random

from telegram import ParseMode
from telethon import Button

from Ava import OWNER_ID, SUPPORT_CHAT
from Ava import telethn as tbot

from ..events import register


@register(pattern="/feedback ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    Ava = (
        "https://telegra.ph/file/27782aafd7609d382098c.jpg",
        "https://telegra.ph/file/f552e5b28dbdcb2d57e62.jpg",
        "https://telegra.ph/file/26a18a0c2244bef31e82a.jpg",
        "https://telegra.ph/file/efba7845c73483c2ef0e4.jpg",
        "https://telegra.ph/file/4c86d4fa7344806d68b1b.jpg",
    )
    NATFEED = ("https://telegra.ph/file/2dd04f407b16bc2cfdf76.jpg",)
    BUTTON = [[Button.url("Go To Support Group", f"https://t.me/{SUPPORT_CHAT}")]]
    TEXT = "ᴛʜᴀɴᴋꜱ ꜰᴏʀ ʏᴏᴜʀ ꜰᴇᴇᴅʙᴀᴄᴋ, ɪ ʜᴏᴘᴇ ʏᴏᴜ ʜᴀᴘᴘʏ ᴡɪᴛʜ ᴏᴜʀ ꜱᴇʀᴠɪᴄᴇ."
    logger_text = f"""
**ɴᴇᴡ ꜰᴇᴇᴅʙᴀᴄᴋ**

**ꜰʀᴏᴍ ᴜꜱᴇʀ:** {mention}
**ᴜꜱᴇʀɴᴀᴍᴇ:** @{e.sender.username}
**ᴜꜱᴇʀ ɪᴅ:** `{e.sender.id}`
**ꜰᴇᴇᴅʙᴀᴄᴋ:** `{e.text}`
"""
    if e.sender_id != OWNER_ID and not quew:
        GIVE = "ɢɪᴠᴇ ꜱᴏᴍᴇ ᴛᴇxᴛ ꜰᴏʀ ꜰᴇᴇᴅʙᴄᴋ ✨"
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=random.choice(NATFEED),
        ),
        return

    await tbot.send_message(
        SUPPORT_CHAT,
        f"{logger_text}",
        file=random.choice(Ava),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(Ava), buttons=BUTTON)
