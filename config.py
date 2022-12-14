from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
API_TOKEN = "5801288802:AAFQkp94h90eL4NXzVf_hd_QnZ0hHerfB5s"

markup = InlineKeyboardMarkup(row_width=2)
insert = InlineKeyboardButton(text="Futbolchi qo'shish",callback_data='insert')
delete = InlineKeyboardButton(text="Barchasini o'chirish",callback_data="delete")
search = InlineKeyboardButton(text="Qidirish",callback_data="search")
markup.add(insert).add(delete).add(search)

class Kiritish(StatesGroup):
    ismi = State()
    telefon_raqam = State()
    raqami = State()
    jamoa = State()
