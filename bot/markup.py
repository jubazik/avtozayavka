from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from gu_12.zayavka import MONTHS

CANCEL = '❌ Отмена'

menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='ГУ-12')]],
    resize_keyboard=True,
)


def wagon_type_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text='Крытые')
    kb.button(text='Полувагоны')
    kb.button(text=CANCEL)
    kb.adjust(2, 1)                      # 2 кнопки в первом ряду, 1 во втором
    return kb.as_markup(resize_keyboard=True)


def month_kb():
    kb = ReplyKeyboardBuilder()
    for m in MONTHS:
        kb.button(text=m.capitalize())   # "январь" → "Январь"
    kb.button(text=CANCEL)
    kb.adjust(3, 3, 3, 3, 1)             # сетка 3×4 + отмена
    return kb.as_markup(resize_keyboard=True)


def decade_kb():
    kb = ReplyKeyboardBuilder()
    for d in ('1', '2', '3'):
        kb.button(text=d)
    kb.button(text=CANCEL)
    kb.adjust(3, 1)
    return kb.as_markup(resize_keyboard=True)


def cancel_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text=CANCEL)
    return kb.as_markup(resize_keyboard=True)