import os
import time

import psutil

import Ava.modules.no_sql.users_db as users_db
from Ava import BOT_NAME, StartTime
from Ava.modules.helper_funcs import formatter

# sᴛᴀᴛs ᴍᴏᴅᴜʟᴇ


async def bot_sys_stats():
    bot_uptime = int(time.time() - StartTime)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    return f"""
▰▰▰▰▰▰▰▰▰▰▰▰▰
➷ {BOT_NAME} ᴜᴘᴛɪᴍᴇ : {formatter.get_readable_time(bot_uptime)}
➷ ʙᴏᴛ ᴄᴀᴘᴀᴄɪᴛʏ : {round(process.memory_info()[0] / 1024**2)} ᴍʙ
➷ ᴄᴘᴜ ᴜsᴀɢᴇ : {cpu}%
➷ ʀᴀᴍ ᴜsᴀɢᴇ : {mem}%
➷ ᴅɪsᴋ ᴜsᴀɢᴇ : {disk}%
➷ ᴜsᴇʀs : 0{users_db.num_users()} ᴜsᴇʀs.
➷ ɢʀᴏᴜᴘs : 0{users_db.num_chats()} ɢʀᴏᴜᴘs.
"""
