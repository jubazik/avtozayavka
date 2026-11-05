from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())  #/start
async def start(message: Message):
    await message.answer(f'Hello {message.from_user.first_name}!', reply_markup=menu)

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile

from bot.markup import menu, CANCEL, wagon_type_kb, month_kb, decade_kb, cancel_kb
from gu_12.zayavka import Zayavka, MONTHS
from gu_12.letter import save_docx

router = Router()


class Gu12(StatesGroup):
    wagon_type = State()
    month = State()
    decade = State()
    wagons = State()


# ---------- Отмена (стоит ПЕРВОЙ, чтобы работала на любом шаге) ----------

@router.message(Command('cancel'))
@router.message(F.text == CANCEL)
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отменено', reply_markup=menu)


# ---------- Общие команды ----------

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'Hello {message.from_user.first_name}!', reply_markup=menu)


@router.message(Command('help'))
async def help_cmd(message: Message):
    await message.answer('Команды: /start, /help, /cancel\nКнопка «ГУ-12» — сформировать заявку')


@router.message(F.text == 'Привет')
async def text_cmd(message: Message):
    await message.reply('И тебе привет')


# ---------- Диалог ГУ-12 ----------

@router.message(F.text == 'ГУ-12')
async def gu12_start(message: Message, state: FSMContext):
    await state.set_state(Gu12.wagon_type)
    await message.answer('Тип вагонов?', reply_markup=wagon_type_kb())


@router.message(Gu12.wagon_type, F.text)
async def gu12_type(message: Message, state: FSMContext):
    wagon_type = message.text.lower()
    if wagon_type not in ('крытые', 'полувагоны'):
        await message.answer('Выберите кнопкой 👇', reply_markup=wagon_type_kb())
        return

    await state.update_data(wagon_type=wagon_type)
    await state.set_state(Gu12.month)
    await message.answer('Месяц?', reply_markup=month_kb())


@router.message(Gu12.month, F.text)
async def gu12_month(message: Message, state: FSMContext):
    month = message.text.lower()
    if month not in MONTHS:
        await message.answer('Выберите месяц кнопкой 👇', reply_markup=month_kb())
        return

    await state.update_data(month=month)
    await state.set_state(Gu12.decade)
    await message.answer('Декада?', reply_markup=decade_kb())


@router.message(Gu12.decade, F.text)
async def gu12_decade(message: Message, state: FSMContext):
    if message.text not in ('1', '2', '3'):
        await message.answer('Выберите 1, 2 или 3 👇', reply_markup=decade_kb())
        return

    await state.update_data(decade=int(message.text))
    await state.set_state(Gu12.wagons)
    await message.answer(
        'Номера вагонов (через пробел или запятую):\nнапример: 29125978, 29126018',
        reply_markup=cancel_kb(),
    )


@router.message(Gu12.wagons, F.text)
async def gu12_wagons(message: Message, state: FSMContext):
    numbers = message.text.replace(',', ' ').split()
    if not numbers:
        await message.answer('Введите хотя бы один номер')
        return

    data = await state.get_data()      # {'wagon_type': ..., 'month': ..., 'decade': ...}
    try:
        z = Zayavka(
            wagon_type=data['wagon_type'],
            wagons=numbers,
            month=data['month'],
            decade=data['decade'],
        )
    except ValueError as e:            # проверка «ровно 8 цифр» из вашего класса
        await message.answer(f'Ошибка: {e}\nВведите номера ещё раз')
        return                         # остаёмся в этом же шаге

    path = save_docx(z)
    await message.answer_document(
        FSInputFile(path),
        caption=f'Заявка ГУ-12: {z.count_text()}',
        reply_markup=menu,
    )
    await state.clear()
@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(f'Команды: /start, /help!')

@router.message(F.text == 'Привет')
async def text_cmd(message: Message):
    await message.reply("И тебе привет")


