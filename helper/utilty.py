from cachetools import TTLCache
from pyrogram import Client
from pyrogram.enums import ChatMembersFilter

admins_lists = TTLCache(maxsize=1024, ttl=600)


async def is_admin_message(bot: Client, chat_id: int, user_id: int) -> bool:
    """
    Check if a message is from an admin of the group or not
    :param chat_id: the chat to check
    :param user_id: the user to check
    :return: True if the message is from an admin, False otherwise
    """

    if chat_id in admins_lists:
        return user_id in admins_lists[chat_id]

    c_admin = [admin.user.id async for admin in bot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)]
    admins_lists[chat_id] = c_admin
    return user_id in admins_lists[chat_id]