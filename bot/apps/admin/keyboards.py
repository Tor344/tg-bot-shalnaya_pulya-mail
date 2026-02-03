from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


start_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="admin",callback_data='admin_inline_keyboard')]])


main_name_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text="firstmail",callback_data='firstmail')],
    [InlineKeyboardButton(
    text="notletters",callback_data='notletters')]])

cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text="Отменить",callback_data='cancel')]])


start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[[KeyboardButton(text="admin",callback_data='admin_keyboard')]])
