import asyncio
import json
import logging
import os
import sys
import time
from functools import wraps
from inspect import getfullargspec
from os import environ, mkdir, path
from sys import exit as sysexit
from traceback import format_exc

import spamwatch
import telegram.ext as tg
from Abg import patch
from aiohttp import ClientSession
from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, PeerIdInvalid
from pyrogram.types import Message
from Python_ARQ import ARQ
from redis import StrictRedis
from telegram import Chat
from telegraph import Telegraph
from telethon import TelegramClient
from telethon.sessions import MemorySession, StringSession

StartTime = time.time()

def get_user_list(__init__, key):
    with open(f"{os.getcwd()}/Ava/{__init__}", "r") as json_file:
        return json.load(json_file)[key]

# enable logging
FORMAT = "[ᴀᴠᴀ] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)

LOGGER = logging.getLogger("[ᴀᴠᴀ]")
LOGGER.info("ᴀᴠᴀʀᴏʙᴏᴛ ɪs sᴛᴀʀᴛɪɴɢ. ")

try:
    if environ.get("ENV"):
        from config import Config
    else:
        from config import Development as Config
except Exception as ef:
    LOGGER.error(ef)  # Print Error
    LOGGER.error(format_exc())
    sysexit(1)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "ʏᴏᴜ ᴍᴜsᴛ ʜᴀᴠᴇ ᴀ ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ ᴏғ ᴀᴛ ʟᴇᴀsᴛ 3.6! ᴍᴜʟᴛɪᴘʟᴇ ғᴇᴀᴛᴜʀᴇs ᴅᴇᴘᴇɴᴅ ᴏɴ ᴛʜɪs. ʙᴏᴛ ǫᴜɪᴛᴛɪɴɢ ʙʏᴇ.",
    )
    sys.exit(1)

# VERS
TOKEN = Config.TOKEN
OWNER_ID = int(Config.OWNER_ID)
JOIN_LOGGER = Config.LOGGER_ID
OWNER_USERNAME = Config.OWNER_USERNAME
DRAGONS = get_user_list("elevated_users.json", "sudos")  # DON'T EDIT
DEV_USERS = get_user_list("elevated_users.json", "devs")  # DON'T EDIT
DEMONS = get_user_list("elevated_users.json", "supports")  # DON'T EDIT
WOLVES = get_user_list("elevated_users.json", "whitelists")  # DON'T EDIT
TIGERS = get_user_list("elevated_users.json", "tigers")  # DON'T EDIT
API_ID = Config.API_ID
API_HASH = Config.API_HASH
DEEP_API = Config.DEEP_API
BAN_STICKER = "CAADBQAD3AcAAor_2VaLJ7V3SdP8dgI"
REDIS_URL = Config.REDIS_URL
SUPPORT_CHAT = Config.SUPPORT_CHAT
MONGO_DB = "Ava"  # DON'T EDIT
MONGO_PORT = "27017"  # DON'T EDIT
MONGO_URI = Config.MONGO_URI
DB_NAME = Config.DB_NAME
BOT_API_URL = "https://api.telegram.org/bot"  # DON'T EDIT
DB_URL = Config.DATABASE_URL
INFOPIC = False
DEBUG = False
EVENT_LOGS = Config.LOGGER_ID
ERROR_LOGS = Config.LOGGER_ID
LOG_GROUP_ID = Config.LOGGER_ID
WEBHOOK = False
URL = ""
PORT = 8443
CERT_PATH = ""
NO_LOAD = []
LOAD = []
DEL_CMDS = True
STRICT_GBAN = True
WORKERS = 8
ALLOW_EXCL = True
TEMP_DOWNLOAD_DIRECTORY = "./Downloads"
REM_BG_API_KEY = "LSdLgCceYz8vNqFgJVzrkDgR"
SPAMWATCH_SUPPORT_CHAT = "Dora_Hub"
SPAMWATCH_API = Config.SPAMWATCH_API
ALLOW_CHATS = True
ARQ_API_URL = "http://arq.hamker.in"
ARQ_API_KEY = Config.ARQ_API_KEY
CUSTOM_CMD = "!"
GENIUS_API_TOKEN = "gIgMyTXuwJoY9VCPNwKdb_RUOA_9mCMmRlbrrdODmNvcpslww_2RIbbWOB8YdBW9"
MOD_USERS = "7044783841"
BACKUP_PASS = 1
WHITELIST_CHATS = []
BL_CHATS = []
SPAMMERS = []

if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("sᴘᴀᴍᴡᴀᴛᴄʜ ᴀᴘɪ ᴋᴇʏ ɪs ᴍɪssɪɴɢ! ʀᴇᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴏɴғɪɢ.")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except Exception:
        sw = None
        LOGGER.warning("ᴄᴀɴ'ᴛ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ sᴘᴀᴍᴡᴀᴛᴄʜ!")

from Ava.modules.sql import SESSION

telegraph = Telegraph()
telegraph.create_account(short_name="Ava")

defaults = tg.Defaults(run_async=True)

updater = tg.Updater(
    token=TOKEN,
    base_url=BOT_API_URL,
    workers=min(32, os.cpu_count() + 4),
    request_kwargs={"read_timeout": 10, "connect_timeout": 10},
    use_context=True,
)
# Telethon
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)

# Dispatcher
dispatcher = updater.dispatcher
session_name = TOKEN.split(":")[0]

# Initialization for Jarvis
Jarvis = Client(
    session_name,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    in_memory=True,
)

# AioHttp Session
aiohttpsession = ClientSession()

# ARQ Client
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
loop = asyncio.get_event_loop()

apps = [Jarvis]

async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for Jarvis in apps:
                if Jarvis != client:
                    try:
                        entity = await Jarvis.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = Jarvis
                        break
            else:
                entity = await Jarvis.get_chat(entity)
                entity_client = Jarvis
    return entity, entity_client

DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# ʙᴏᴛ ɪɴғᴏ
print("[INFO]: ɢᴇᴛᴛɪɴɢ ʙᴏᴛ ɪɴғᴏ...")
BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username

async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})

from Ava.modules.helper_funcs.handlers import CustomMessageHandler, CustomRegexHandler

tg.RegexHandler = CustomRegexHandler
tg.MessageHandler = CustomMessageHandler

from Ava.modules.helper_funcs.handlers import CustomCommandHandler

if CUSTOM_CMD and len(CUSTOM_CMD) >= 1:
    tg.CommandHandler = CustomCommandHandler

try:
    from Ava.antispam import antispam_cek_user, antispam_restrict_user, detect_user

    LOGGER.info("ɴᴏᴛᴇ: ᴀɴᴛɪsᴘᴀᴍ ʟᴏᴀᴅᴇᴅ!")
    antispam_module = True
except ModuleNotFoundError:
    antispam_module = False

def spamcheck(func):
    @wraps(func)
    def check_user(update, context, *args, **kwargs):
        chat = update.effective_chat
        user = update.effective_user
        message = update.effective_message
        # If not user, return function
        if not user:
            return func(update, context, *args, **kwargs)
        # If msg from self, return True
        if user and user.id == context.bot.id:
            return False
        if DEBUG:
            print(
                "{} | {} | {} | {}".format(
                    message.text or message.caption,
                    user.id,
                    message.chat.title,
                    chat.id,
                )
            )
        if antispam_module:
            parsing_date = time.mktime(message.date.timetuple())
            detecting = detect_user(user.id, chat.id, message, parsing_date)
            if detecting:
                return False
            antispam_restrict_user(user.id, parsing_date)
        if int(user.id) in SPAMMERS:
            if DEBUG:
                print("^ ᴛʜɪs ᴜsᴇʀ ɪs sᴘᴀᴍᴍᴇʀ!")
            return False
        elif int(chat.id) in BL_CHATS:
            dispatcher.bot.sendMessage(
                chat.id, "ᴛʜɪs ɢʀᴏᴜᴘ ɪs ɪɴ ʙʟᴀᴄᴋʟɪsᴛ, i'ᴍ ʟᴇᴀᴠɪɴɢ..."
            )
            dispatcher.bot.leaveChat(chat.id)
            return False
        return func(update, context, *args, **kwargs)

    return check_user
