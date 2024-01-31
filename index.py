import os

from pyrogram.client import Client
from pyrogram import filters
from pyrogram.errors import ChatAdminRequired, MessageDeleteForbidden
from pyrogram.types import Message, CallbackQuery
from helper import database, callback_menu, utilty
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", 000))  # get it from my.telegram.org
API_HASH = os.environ.get("API_HASH", "") # get it from my.telegram.org
BOT_TOKEN = os.environ.get("BOT_TOKEN", "") # get it from @BotFather


bot = Client("block-channel", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@bot.on_message(filters.command(["start", "help"]) & filters.private)
async def welcome_private(_, message: Message):
    await message.reply("חוסם כתיבה כערוצים/קבוצות בצאט 🤖!")


@bot.on_message(filters.command(["start", "help"]) & filters.group)
async def welcome_group(_, message: Message):
    c_id = message.chat.id
    try:
        user_id = message.from_user.id
    except AttributeError:
        user_id = message.sender_chat.id
    if not await utilty.is_admin_message(bot, c_id, user_id):
        try:
            await message.delete()
        except MessageDeleteForbidden:
            pass
        return
    await message.reply(
        "חוסם כתיבה כערוצים\קבוצות בצאט 🤖! \nנא לוודא שיש לי אפשרות מחיקה והסרת משתמשים לפעילות תקינה של הבוט")


@bot.on_callback_query(filters=filters.regex("^link:"))
async def link_callback(_, callback: CallbackQuery):
    u_id = callback.from_user.id
    c_id = callback.message.chat.id
    if not await utilty.is_admin_message(bot, c_id, u_id):
        await callback.answer("אתה לא מנהל!")
        return
    try:
        ignore_id = int(callback.data.split(":")[1])
    except (ValueError, IndexError):
        await callback.answer("ID לא תקין!")
        return

    if database.create_new_ignore_id(chat_id=c_id, ignore_id=ignore_id):
        await callback.edit_message_text("מזהה קבוצה/ערוץ מקושר נוסף לרשימה לבנה")
    else:
        await callback.edit_message_text("מזהה קבוצה/ערוץ מקושר כבר ברשימה לבנה")


@bot.on_callback_query(filters=filters.regex("^unlink:"))
async def unlink_callback(_, callback: CallbackQuery):
    u_id = callback.from_user.id
    c_id = callback.message.chat.id
    if not await utilty.is_admin_message(bot, c_id, u_id):
        await callback.answer("אתה לא מנהל!")
        return
    try:
        ignore_id = int(callback.data.split(":")[1])
    except (ValueError, IndexError):
        await callback.answer("ID לא תקין!")
        return

    if database.remove_ignore_id(chat_id=c_id, ignore_id=ignore_id):
        await callback.edit_message_text("מזהה קבוצה/ערוץ הוסר מרשימה לבנה")
    else:
        await callback.edit_message_text("מזהה קבוצה/ערוץ לא נמצא ברשימה לבנה")


@bot.on_message(filters.command("link") & filters.group)
async def linked_channel(c: Client, message: Message):
    c_id = message.chat.id
    try:
        user_id = message.from_user.id
    except AttributeError:
        user_id = message.sender_chat.id

    try:
        ignore_id = int(message.command[1])
    except (ValueError, IndexError):
        ignore_id = None

    if str(user_id).startswith("-1") and ignore_id is not None:
        await c.send_message(c_id, text="כדי להוסיף id לרשימה לבנה עליך ללחוץ על כפתור האימות",
                             reply_markup=callback_menu.link_button(ignore_id))
        return
    elif str(user_id).startswith("-1") and ignore_id is None:
        try:
            await message.delete()
        except MessageDeleteForbidden:
            pass
        return
    elif not await utilty.is_admin_message(bot, c_id, user_id):
        await message.reply("אתה לא מנהל!")
        return

    if ignore_id is None:
        await message.reply("נא לספק id תקין")
        return

    if database.create_new_ignore_id(chat_id=c_id, ignore_id=ignore_id):
        await message.reply("מזהה קבוצה/ערוץ נוסף לרשימה לבנה")
    else:
        await message.reply("מזהה קבוצה/ערוץ כבר ברשימה לבנה")


@bot.on_message(filters.command("unlink") & filters.group)
async def unlinked_channel(c: Client, message: Message):
    c_id = message.chat.id
    try:
        user_id = message.from_user.id
    except AttributeError:
        user_id = message.sender_chat.id

    try:
        ignore_id = int(message.command[1])
    except (ValueError, IndexError):
        ignore_id = None

    if str(user_id).startswith("-1") and ignore_id is not None:
        await c.send_message(c_id, text="כדי להסיר id מרשימה לבנה עליך ללחוץ על כפתור האימות",
                             reply_markup=callback_menu.unlink_button(ignore_id))
        return
    elif str(user_id).startswith("-1") and ignore_id is None:
        try:
            await message.delete()
        except MessageDeleteForbidden:
            pass
        return
    elif not await utilty.is_admin_message(bot, c_id, user_id):
        await message.reply("אתה לא מנהל!")
        return
    if ignore_id is None:
        await message.reply("נא לספק id תקין")
        return

    if database.remove_ignore_id(chat_id=c_id, ignore_id=ignore_id):
        await message.reply("מזהה ערוץ מקושר הוסר מרשימה לבנה")
    else:
        await message.reply("מזהה ערוץ לא נמצא ברשימה לבנה")


@bot.on_message(filters.sender_chat & filters.group)
async def block_channel(c: Client, message: Message):
    sender_id = message.sender_chat.id
    c_id = message.chat.id
    if sender_id == c_id or sender_id in database.get_all_ignore_ids(c_id):
        return
    else:
        try:
            await c.ban_chat_member(chat_id=c_id, user_id=sender_id)
        except ChatAdminRequired:
            await message.reply("כדי שאוכל להסיר ערוצים נא לתת לי הרשאות מחיקת והסרת משתמשים",
                                reply_markup=callback_menu.admin_button_request(bot.me.username))
            return

        try:
            await message.delete()
        except MessageDeleteForbidden:
            pass


if __name__ == '__main__':
    bot.run()
