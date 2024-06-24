import requests

from Ava import SUPPORT_CHAT
from Ava.events import register as uvbot


@uvbot(pattern="[/!]dare")
async def _(asux):
    try:
        ak = requests.get("https://api.truthordarebot.xyz/v1/dare").json()
        results = f"{ak['question']}"
        return await asux.reply(results)
    except Exception:
        await asux.reply(f"ᴇʀʀᴏʀ ʀᴇᴘᴏʀᴛ @{SUPPORT_CHAT}")


@uvbot(pattern="[/!]truth")
async def _(asux):
    try:
        ak = requests.get("https://api.truthordarebot.xyz/v1/truth").json()
        results = f"{ak['question']}"
        return await asux.reply(results)
    except Exception:
        await asux.reply(f"ᴇʀʀᴏʀ ʀᴇᴘᴏʀᴛ @{SUPPORT_CHAT}")


__mod_name__ = "𝐓ʀᴜᴛʜ-Dᴀʀᴇ"

from Ava.modules.language import gs


def get_help(chat):
    return gs(chat, "td_help")
