import time
from typing import List

import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext

from Ava import Jarvis as app
from Ava import StartTime, dispatcher
from Ava.modules.disable import DisableAbleCommandHandler
from Ava.modules.helper_funcs.chat_status import sudo_plus
from Ava.modules.stats import bot_sys_stats as uvstats

sites_list = {
    "Telegram": "https://api.telegram.org",
    "Kaizoku": "https://animekaizoku.com",
    "Kayo": "https://animekayo.com",
    "Jikan": "https://api.jikan.moe/v3",
    "Kuki Chatbot": "https://kuki-yukicloud.up.railway.app/",
    "liones API": "https://liones-api.herokuapp.com/",
}


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "ᴍ", "ʜ", "ᴅᴀʏs"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += f"{time_list.pop()}, "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


def ping_func(to_ping: List[str]) -> List[str]:
    ping_result = []

    for each_ping in to_ping:
        start_time = time.time()
        site_to_ping = sites_list[each_ping]
        r = requests.get(site_to_ping)
        end_time = time.time()
        ping_time = f"{str(round(end_time - start_time, 2))}s"

        pinged_site = f"<b>{each_ping}</b>"

        if each_ping in ("Kaizoku", "Kayo"):
            pinged_site = f'<a href="{sites_list[each_ping]}">{each_ping}</a>'
            ping_time = f"<code>{ping_time} (Status: {r.status_code})</code>"

        ping_text = f"{pinged_site}: <code>{ping_time}</code>"
        ping_result.append(ping_text)

    return ping_result


# @sudo_plus   # ᴘᴜʙʟɪᴄ ᴘɪɴɢ ᴄᴏᴍᴍᴀɴᴅ
def ping(update: Update, context: CallbackContext):
    msg = update.effective_message

    start_time = time.time()
    message = msg.reply_text("Pinging...")
    end_time = time.time()
    telegram_ping = f"{str(round((end_time - start_time) * 1000, 3))} ms"
    uptime = get_readable_time((time.time() - StartTime))

    message.edit_text(
        f"PONG!!\n<b>ᴛɪᴍᴇ ᴛᴀᴋᴇɴ:</b> <code>{telegram_ping}</code>\n<b>sᴇʀᴠɪᴄᴇ ᴜᴘᴛɪᴍᴇ:</b> <code>{uptime}</code>",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="sʏsᴛᴇᴍ sᴛᴀᴛs", callback_data="stats_callback"
                    )
                ]
            ]
        ),
    )


@app.on_callback_query(filters.regex("stats_callback"))
async def stats_callback(_, CallbackQuery):
    text = await uvstats()
    await app.answer_callback_query(CallbackQuery.id, text, show_alert=True)


@sudo_plus
def pingall(update: Update, context: CallbackContext):
    to_ping = ["Kaizoku", "Kayo", "Telegram", "Jikan", "Kuki Chatbot", "liones API"]
    pinged_list = ping_func(to_ping)
    pinged_list.insert(2, "")
    uptime = get_readable_time((time.time() - StartTime))

    reply_msg = "⏱ Ping results are:\n" + "\n".join(pinged_list)
    reply_msg += f"\n<b>Service uptime:</b> <code>{uptime}</code>"

    update.effective_message.reply_text(
        reply_msg,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


PING_HANDLER = DisableAbleCommandHandler("ping", ping, run_async=True)
PINGALL_HANDLER = DisableAbleCommandHandler("pingall", pingall, run_async=True)

dispatcher.add_handler(PING_HANDLER)
dispatcher.add_handler(PINGALL_HANDLER)

__command_list__ = ["ping", "pingall"]
__handlers__ = [PING_HANDLER, PINGALL_HANDLER]


__mod_name__ = "𝐏ɪɴɢ"

from Ava.modules.language import gs

def get_help(chat):
    return gs(chat, "ping_help")
