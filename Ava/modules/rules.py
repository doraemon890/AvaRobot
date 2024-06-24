from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters
from telegram.utils.helpers import escape_markdown

import Ava.modules.sql.rules_sql as sql
from Ava import dispatcher
from Ava.modules.helper_funcs.anonymous import AdminPerms, user_admin
from Ava.modules.helper_funcs.decorators import Avacmd
from Ava.modules.helper_funcs.string_handling import markdown_parser


@Avacmd(command="rules", filters=Filters.chat_type.groups)
def get_rules(update: Update, _: CallbackContext):
    chat_id = update.effective_chat.id
    send_rules(update, chat_id)


# Do not async - not from a handler
def send_rules(update, chat_id, from_pm=False):
    bot = dispatcher.bot
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message
    reply_msg = update.message.reply_to_message
    try:
        chat = bot.get_chat(chat_id)
    except BadRequest as excp:
        if excp.message == "Chat not found" and from_pm:
            bot.send_message(
                user.id,
                "ᴛʜᴇ ʀᴜʟᴇꜱ ꜱʜᴏʀᴛᴄᴜᴛ ꜰᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ ʜᴀꜱɴ'ᴛ ʙᴇᴇɴ ꜱᴇᴛ ᴘʀᴏᴘᴇʀʟʏ! ᴀꜱᴋ ᴀᴅᴍɪɴꜱ ᴛᴏ "
                "ꜰɪx ᴛʜɪꜱ.\nᴍᴀʏ ʙᴇ ᴛʜᴇʏ ꜰᴏʀɢᴏᴛ ᴛʜᴇ ʜʏᴘʜᴇɴ ɪɴ ɪᴅ",
            )
            return
        raise

    rules = sql.get_rules(chat_id)
    text = f"ᴛʜᴇ ʀᴜʟᴇꜱ ꜰᴏʀ *{escape_markdown(chat.title)}* ᴀʀᴇ:\n\n{rules}"

    if from_pm and rules:
        bot.send_message(
            user.id,
            text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif from_pm:
        bot.send_message(
            user.id,
            "ᴛʜᴇ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴꜱ ʜᴀᴠᴇɴ'ᴛ ꜱᴇᴛ ᴀɴʏ ʀᴜʟᴇꜱ ꜰᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ ʏᴇᴛ. "
            "ᴛʜɪꜱ ᴘʀᴏʙᴇʙʟʏ ᴅᴏᴇꜱ'ᴛ ᴍᴇᴀɴ ɪᴛ'ꜱ ʟᴀᴡʟᴇꜱꜱ ᴛʜᴏᴜɢʜ...!",
        )
    elif rules and reply_msg:
        reply_msg.reply_text(
            "ᴘʟᴇᴀꜱᴇ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ꜱᴇᴇ ᴛʜᴇ ʀᴜʟᴇꜱ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="📝 ʀᴇᴀᴅ ʀᴜʟᴇꜱ",
                            url=f"t.me/{bot.username}?start={chat_id}",
                        ),
                        InlineKeyboardButton(text="❌ ᴅᴇʟᴇᴛᴇ", callback_data="close2"),
                    ]
                ]
            ),
        )
    elif rules:
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📝 ʀᴇᴀᴅ ʀᴜʟᴇꜱ",
                        url=f"t.me/{bot.username}?start={chat_id}",
                    ),
                    InlineKeyboardButton(text="❌ ᴅᴇʟᴇᴛᴇ", callback_data="close2"),
                ]
            ]
        )
        txt = "Please click the button below to see the rules."
        if not message.reply_to_message:
            message.reply_text(txt, reply_markup=btn)

        if message.reply_to_message:
            message.reply_to_message.reply_text(txt, reply_markup=btn)
    else:
        update.effective_message.reply_text(
            "ᴛʜᴇ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴꜱ ʜᴀᴠᴇɴ'ᴛ ꜱᴇᴛ ᴀɴʏ ʀᴜʟᴇꜱ ꜰᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ ʏᴇᴛ. "
            "ᴛʜɪꜱ ᴘʀᴏʙᴀʙʟʏ ᴅᴏᴇꜱ'ᴛ ᴍᴇᴀɴ ɪᴛꜱ ʟᴀᴡʟᴇꜱꜱ ᴛʜᴏᴜɢʜ...!",
        )


close_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("❌ ᴅᴇʟᴇᴛᴇ", callback_data="close2")]]
)


@Avacmd(command="setrules", filters=Filters.chat_type.groups)
@user_admin(AdminPerms.CAN_CHANGE_INFO)
def set_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message  # type: Optional[Message]
    raw_text = msg.text
    args = raw_text.split(None, 1)  # use python's maxsplit to separate cmd and args
    if len(args) == 2:
        txt = args[1]
        offset = len(txt) - len(raw_text)  # set correct offset relative to command
        markdown_rules = markdown_parser(
            txt,
            entities=msg.parse_entities(),
            offset=offset,
        )

        sql.set_rules(chat_id, markdown_rules)
        update.effective_message.reply_text("ꜱᴜᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ʀᴜʟᴇꜱ ꜰᴏʀ ᴛʜɪꜱ ɢʀᴏᴜᴘ.")


@Avacmd(command="clearrules", filters=Filters.chat_type.groups)
@user_admin(AdminPerms.CAN_CHANGE_INFO)
def clear_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    sql.set_rules(chat_id, "")
    update.effective_message.reply_text("ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʟᴇᴀʀᴇᴅ ʀᴜʟᴇꜱ!")


def __stats__():
    return f"× {sql.num_chats()} chats have rules set."


def __import_data__(chat_id, data):
    # set chat rules
    rules = data.get("info", {}).get("rules", "")
    sql.set_rules(chat_id, rules)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    return f"This chat has had it's rules set: `{bool(sql.get_rules(chat_id))}`"


__mod_name__ = "𝐑ᴜʟᴇs"

from Ava.modules.language import gs

def get_help(chat):
    return gs(chat, "rules_help")
