import datetime
import html
import platform
import time
from platform import python_version

import requests
from psutil import boot_time, cpu_percent, disk_usage, virtual_memory
from telegram import (
    MAX_MESSAGE_LENGTH,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MessageEntity,
    ParseMode,
    Update,
)
from telegram import __version__ as ptbver
from telegram.error import BadRequest
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown, mention_html
from telethon import events
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins

import Ava.modules.sql.userinfo_sql as sql
from Ava import (
    DEV_USERS,
    INFOPIC,
    OWNER_ID,
    StartTime,
    dispatcher,
    sw,
)
from Ava import telethn as Ava
from Ava.__main__ import STATS, TOKEN, USER_INFO
from Ava.modules.helper_funcs.chat_status import sudo_plus
from Ava.modules.helper_funcs.decorators import Avacallback, Avacmd
from Ava.modules.helper_funcs.extraction import extract_user
from Ava.modules.no_sql.global_bans_db import is_user_gbanned
from Ava.modules.no_sql.users_db import get_user_num_chats
from Ava.modules.sql import SESSION


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


@Avacmd(command="id")
def get_id(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    msg = update.effective_message
    if user_id := extract_user(msg, args):
        if msg.reply_to_message and msg.reply_to_message.forward_from:
            user1 = message.reply_to_message.from_user
            user2 = message.reply_to_message.forward_from

            msg.reply_text(
                f"× <b>ꜱᴇɴᴅᴇʀ:</b> {mention_html(user2.id, user2.first_name)} - <code>{user2.id}</code>.\n"
                f"× <b>ꜰᴏʀᴡᴀʀᴅᴇʀ:</b> {mention_html(user1.id, user1.first_name)} - <code>{user1.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

        else:
            user = bot.get_chat(user_id)
            msg.reply_text(
                f"× <b>ʀᴇᴘʟɪᴇᴅ ᴛᴏ:</b> {mention_html(user.id, user.first_name)}\n× <b>ID of the user:</b> <code>{user.id}</code>",
                parse_mode=ParseMode.HTML,
            )

    elif chat.type == "private":
        msg.reply_text(
            f"⟃ ʏᴏᴜʀ ɪᴅ ɪꜱ <code>{chat.id}</code>.", parse_mode=ParseMode.HTML
        )

    else:
        msg.reply_text(
            f"⟃ <b>ᴜꜱᴇʀ:</b> {mention_html(msg.from_user.id, msg.from_user.first_name)}\n⟃ <b>ꜰʀᴏᴍ ᴜꜱᴇʀ ɪᴅ:</b> <code>{update.effective_message.from_user.id}</code>\n⟃ <b>ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪᴅ:</b> <code>{chat.id}</code>",
            parse_mode=ParseMode.HTML,
        )


@Ava.on(
    events.NewMessage(
        pattern="/ginfo ",
        from_users=DEV_USERS,
    ),
)
async def group_info(event) -> None:
    chat = event.text.split(" ", 1)[1]
    try:
        entity = await event.client.get_entity(chat)
        totallist = await event.client.get_participants(
            entity,
            filter=ChannelParticipantsAdmins,
        )
        ch_full = await event.client(GetFullChannelRequest(channel=entity))
    except Exception:
        await event.reply(
            "Can't for some reason, maybe it is a private one or that I am banned there.",
        )
        return
    msg = f"**ɪᴅ**: `{entity.id}`"
    msg += f"\n**ᴛɪᴛʟᴇ**: `{entity.title}`"
    msg += f"\n**ᴅᴀᴛᴀᴄᴇɴᴛᴇʀ**: `{entity.photo.dc_id}`"
    msg += f"\n**ᴠɪᴅᴇᴏ ᴘꜰᴘ**: `{entity.photo.has_video}`"
    msg += f"\n**ꜱᴜᴘᴇʀɢʀᴏᴜᴘ**: `{entity.megagroup}`"
    msg += f"\n**ʀᴇꜱᴛʀɪᴄᴛᴇᴅ**: `{entity.restricted}`"
    msg += f"\n**ꜱᴄᴀᴍ**: `{entity.scam}`"
    msg += f"\n**ꜱʟᴏᴡᴍᴏᴅᴇ**: `{entity.slowmode_enabled}`"
    if entity.username:
        msg += f"\n**ᴜꜱᴇʀɴᴀᴍᴇ**: {entity.username}"
    msg += "\n\n**ᴍᴇᴍʙᴇʀ ꜱᴛᴀᴛꜱ:**"
    msg += f"\n`ᴀᴅᴍɪɴꜱ:` `{len(totallist)}`"
    msg += f"\n`ᴜꜱᴇʀꜱ`: `{totallist.total}`"
    msg += "\n\n**ᴀᴅᴍɪɴꜱ ʟɪꜱᴛ:**"
    for x in totallist:
        msg += f"\n• [{x.id}](tg://user?id={x.id})"
    msg += f"\n\n**ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ**:\n`{ch_full.full_chat.about}`"
    await event.reply(msg)


@Avacmd(command="gifid")
def gifid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.animation:
        update.effective_message.reply_text(
            f"ɢɪꜰ ɪᴅ:\n<code>{msg.reply_to_message.animation.file_id}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text("Please reply to a gif to get its ID.")


@Avacmd(command=["info"])
def info(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].isdigit()
            and not message.parse_entities([MessageEntity.TEXT_MENTION])
        )
    ):
        message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴇxᴛʀᴀᴄᴛ ᴀ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴛʜɪꜱ.")
        return

    else:
        return

    rep = message.reply_text("<code>ɢᴇᴛᴛɪɴɢ ᴜsᴇʀ ᴅᴀᴛᴀ...</code>", parse_mode=ParseMode.HTML)

    text = (
        f"┏━━━━━❰ <b>ʜᴇʀᴇ's ᴛʜᴇ ᴜsᴇʀ ᴅᴀᴛᴀ:</b>❱━━━━━┓\n\n"
        f"➻ ɪᴅ: <code>{user.id}</code>\n"
        f"➻ ꜰɪʀꜱᴛ ɴᴀᴍᴇ: {html.escape(user.first_name)}"
    )

    if user.last_name:
        text += f"\n➻ ʟᴀꜱᴛ ɴᴀᴍᴇ: {html.escape(user.last_name)}"

    if user.username:
        text += f"\n➻ ᴜꜱᴇʀɴᴀᴍᴇ: @{html.escape(user.username)}"

    text += f"\n➻ ʟɪɴᴋ: {mention_html(user.id, 'link')}"

    if chat.type != "private" and user_id != bot.id:
        _stext = "\n➻ <b>ᴩʀᴇsᴇɴᴄᴇ:</b> <code>{}</code>"

        status = bot.get_chat_member(chat.id, user.id).status
        if status:
            if status in {"left", "kicked"}:
                text += _stext.format("ɴᴏᴛ ʜᴇʀᴇ")
            elif status == "member":
                text += _stext.format("ᴅᴇᴛᴇᴄᴛᴇᴅ")
            elif status in {"administrator", "creator"}:
                text += _stext.format("ᴀᴅᴍɪɴ")

    try:
        if spamwtc := sw.get_ban(int(user.id)):
            text += "\n\n<b>ᴛʜɪs ᴘᴇʀsᴏɴ ɪs sᴘᴀᴍᴡᴀᴛᴄʜᴇᴅ!</b>"
            text += f"\nʀᴇᴀꜱᴏɴ: <pre>{spamwtc.reason}</pre>"
            text += "\nᴀᴘᴘᴇᴀʟ ᴀᴛ [sᴜᴘᴘᴏʀᴛ](https://t.me/Dora_Hub)"
    except Exception:
        pass  # don't crash if api is down somehow...

    try:
        user_member = chat.get_member(user.id)
        if user_member.status == "administrator":
            result = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}",
            )
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result["custom_title"]
                text += f"\n\nᴛɪᴛʟᴇ:\n<b>{custom_title}</b>"
    except BadRequest:
        pass

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    if INFOPIC:
        try:
            profile = context.bot.get_user_profile_photos(user.id).photos[0][-1]
            context.bot.sendChatAction(chat.id, "upload_photo")
            context.bot.send_photo(
                chat.id,
                photo=profile,
                caption=(text),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )

        # Incase user don't have profile pic, send normal text
        except IndexError:
            message.reply_text(
                text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
    else:
        message.reply_text(
            text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )

    rep.delete()


@Avacmd(command="me")
def about_me(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user_id = extract_user(message, args)

    user = bot.get_chat(user_id) if user_id else message.from_user
    if info := sql.get_user_me_info(user.id):
        update.effective_message.reply_text(
            f"*{user.first_name}*:\n{escape_markdown(info)}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text(
            f"{username} ʜᴀꜱɴ'ᴛ ꜱᴇᴛ ᴀɴ ɪɴꜰᴏ ᴍᴇꜱꜱᴀɢᴇ ᴀʙᴏᴜᴛ ᴛʜᴇᴍꜱᴇʟᴠᴇꜱ ʏᴇᴛ!",
        )
    else:
        update.effective_message.reply_text(
            "ᴛʜᴇʀᴇ ɪꜱ ɴᴏᴛ ᴀɴʏ ʙɪᴏ, use /setme ᴛᴏ ꜱᴇᴛ ᴏɴᴇ."
        )


@Avacmd(command="setme")
def set_about_me(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = message.from_user.id
    if user_id in [777000, 1087968824]:
        message.reply_text("Error! Unauthorized")
        return
    bot = context.bot
    if message.reply_to_message:
        repl_message = message.reply_to_message
        repl_user_id = repl_message.from_user.id
        if repl_user_id in [bot.id, 777000, 1087968824] and (user_id in DEV_USERS):
            user_id = repl_user_id
    text = message.text
    info = text.split(None, 1)
    if len(info) == 2:
        if len(info[1]) < MAX_MESSAGE_LENGTH // 4:
            sql.set_user_me_info(user_id, info[1])
            if user_id in [777000, 1087968824]:
                message.reply_text("Authorized...Information updated!")
            elif user_id == bot.id:
                message.reply_text("I have updated my info with the one you provided!")
            else:
                message.reply_text("Information updated!")
        else:
            message.reply_text(
                f"The info needs to be under {MAX_MESSAGE_LENGTH // 4} characters! You have {len(info[1])}."
            )


@Avacmd(command="stats", can_disable=True)
@sudo_plus
def stats(update, context):
    db_size = SESSION.execute(
        "SELECT pg_size_pretty(pg_database_size(current_database()))"
    ).scalar_one_or_none()
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    botuptime = get_readable_time((time.time() - StartTime))
    status = "*「 ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛɪᴄꜱ: 」*\n\n"
    status += f"*× ꜱʏꜱᴛᴇᴍ ꜱᴛᴀʀᴛ ᴛɪᴍᴇ:* {str(uptime)}" + "\n"
    uname = platform.uname()
    status += f"*× ꜱʏꜱᴛᴇᴍ:* {str(uname.system)}" + "\n"
    status += f"*× ɴᴏᴅᴇ ɴᴀᴍᴇ:* {escape_markdown(str(uname.node))}" + "\n"
    status += f"*× ʀᴇʟᴇᴀꜱᴇ:* {escape_markdown(str(uname.release))}" + "\n"
    status += f"*× ᴍᴀᴄʜɪɴᴇ:* {escape_markdown(str(uname.machine))}" + "\n"

    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += f"*× ᴄᴘᴜ:* {str(cpu)}" + " %\n"
    status += f"*× ʀᴀᴍ:* {str(mem[2])}" + " %\n"
    status += f"*× ꜱᴛᴏʀᴀɢᴇ:* {str(disk[3])}" + " %\n\n"
    status += f"*× ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ:* {python_version()}" + "\n"
    status += f"*× ᴘʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ:* {str(ptbver)}" + "\n"
    status += f"*× ᴜᴘᴛɪᴍᴇ:* {str(botuptime)}" + "\n"
    status += f"*× ᴅʙ ꜱɪᴢᴇ:* {str(db_size)}" + "\n"
    kb = [[InlineKeyboardButton("Ping", callback_data="pingCB")]]

    try:
        update.effective_message.reply_text(
            status
            + "\n*ʙᴏᴛ sᴛᴀᴛsɪsᴛɪᴄs*:\n"
            + "\n".join([mod.__stats__() for mod in STATS])
            + "\n\n[ɢɪᴛʜᴜʙ](https://github.com/doraemon890/AvaRobot)\n\n "
            + "🥀ʙʏ [ᴊᴀʀᴠɪs](github.com/doraemon890)\n",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(kb),
            disable_web_page_preview=True,
        )
    except BaseException:
        update.effective_message.reply_text(
            (
                (
                    (
                        "\n*ʙᴏᴛ sᴛᴀᴛsɪsᴛɪᴄs*:\n"
                        + "\n".join(mod.__stats__() for mod in STATS)
                    )
                    + "\n\n[ɢɪᴛʜᴜʙ](https://github.com/doraemon890/AvaRobot)\n\n"
                )
                + "🥀ʙʏ [ᴊᴀʀᴠɪs](github.com/doraemon890)\n"
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(kb),
            disable_web_page_preview=True,
        )


@Avacallback(pattern=r"^pingCB")
def pingCallback(update: Update, context: CallbackContext):
    query = update.callback_query
    start_time = time.time()
    requests.get("https://api.telegram.org")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    query.answer(f"ᴘᴏɴɢ 🌺! {ping_time}ms")


@Avacmd(command="bio")
def about_bio(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    user_id = extract_user(message, args)
    user = bot.get_chat(user_id) if user_id else message.from_user
    if info := sql.get_user_bio(user.id):
        update.effective_message.reply_text(
            f"*{user.first_name}*:\n{escape_markdown(info)}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = user.first_name
        update.effective_message.reply_text(
            f"{username} ʜᴀꜱɴ'ᴛ ʜᴀᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ꜱᴇᴛ ᴀʙᴏᴜᴛ ᴛʜᴇᴍꜱᴇʟᴠᴇꜱ ʏᴇᴛ!\nꜱᴇᴛ ᴏɴᴇ ᴜɪsɪɴɢ  /setbio",
        )
    else:
        update.effective_message.reply_text(
            "ʏᴏᴜ ʜᴀꜱɴ' ʜᴀᴅ ᴀ ʙɪᴏ ꜱᴇᴛ ᴀʙᴏᴜᴛ ʏᴏᴜʀꜱᴇʟꜰ ʏᴇᴛ!",
        )


@Avacmd(command="setbio")
def set_about_bio(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot

    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id

        if user_id == message.from_user.id:
            message.reply_text(
                "ʜᴀ, ʏᴏᴜ ᴄᴀɴ'ᴛ ꜱᴇᴛ ʏᴏᴜʀ ᴏᴡɴ ʙɪᴏ! ʏᴏᴜ'ʀᴇ ᴀᴛ ᴛʜᴇ ᴍᴇʀᴄʏ ᴏꜰ ᴏᴛʜᴇʀꜱ ʜᴇʀᴇ...",
            )
            return

        if user_id in [777000, 1087968824] and sender_id not in DEV_USERS:
            message.reply_text("You are not authorised")
            return

        if user_id == bot.id and sender_id not in DEV_USERS:
            message.reply_text(
                "ᴇʀᴍ... ʏᴇᴀʜ, ɪ ᴏɴʟʏ ᴛʀᴜꜱᴛ ᴛʜᴇ ᴀᴄᴋᴇʀᴍᴀɴꜱ ᴛᴏ ꜱᴇᴛ ᴍʏ ʙɪᴏ.",
            )
            return

        text = message.text
        bio = text.split(
            None,
            1,
        )  # use python's maxsplit to only remove the cmd, hence keeping newlines.

        if len(bio) == 2:
            if len(bio[1]) < MAX_MESSAGE_LENGTH // 4:
                sql.set_user_bio(user_id, bio[1])
                message.reply_text(f"Updated {repl_message.from_user.first_name}'s bio!")
            else:
                message.reply_text(
                    f"ʙɪᴏ ɴᴇᴇᴅꜱ ᴛᴏ ᴜɴᴅᴇʀ {MAX_MESSAGE_LENGTH // 4} ᴄʜᴀʀᴀᴄᴛᴇʀ! ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ ꜱᴇᴛ {len(bio[1])}."
                )
    else:
        message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ꜱᴏᴍᴇᴏɴᴇ ᴛᴏ ꜱᴇᴛ ᴛʜᴇɪʀ ʙɪᴏ!")


def __user_info__(user_id):
    bio = html.escape(sql.get_user_bio(user_id) or "")
    me = html.escape(sql.get_user_me_info(user_id) or "")
    result = ""
    if me:
        result += f"<b>ᴀʙᴏᴜᴛ ᴜꜱᴇʀ:</b>\n{me}\n"
    if bio:
        result += f"<b>ᴡʜᴀᴛ ᴏᴛʜᴇʀ ꜱᴀʏꜱ:</b>\n{bio}\n"
    result = result.strip("\n")
    return result


__mod_name__ = "𝐈ɴғᴏ "

from Ava.modules.language import gs


def get_help(chat):
    return gs(chat, "userinfo_help")
