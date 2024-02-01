from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def link_button(ignore_id: int):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="אימות ניהול", callback_data=f"link:{ignore_id}")
            ]
        ]
    )


def unlink_button(ignore_id: int):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="אימות ניהול", callback_data=f"unlink:{ignore_id}")
            ]
        ]
    )


def admin_button_request(username: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="הפוך למנהל",
                                     url=f"https://t.me/{username}?startgroup=start&admin=delete_messages+restrict_members")
            ]
        ]
    )


def request_join_button(username: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="הוסף אותי לקבוצה",
                                     url=f"https://t.me/{username}?startgroup=start&admin=delete_messages+restrict_members")
            ]
        ]
    )
