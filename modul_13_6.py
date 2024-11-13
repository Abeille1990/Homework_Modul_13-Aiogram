from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
from time import sleep

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

rkb = ReplyKeyboardMarkup(resize_keyboard=True)
ikb = InlineKeyboardMarkup(resize_keyboard=True)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


rbutton = KeyboardButton(text='Что я умею?')

ibutton1 = InlineKeyboardButton(text='Расчитать норму калорий', callback_data="count")
ibutton2 = InlineKeyboardButton(text='Формула расчета калорий', callback_data="formulas")


rkb.add(rbutton)
ikb.row(ibutton1, ibutton2)

inline_menu = ikb


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=rkb)


@dp.message_handler(text='Что я умею?')
async def main_menu(message):
    await message.answer("А вот что:", reply_markup=ikb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(f'Раcчет производится по формуле Миффлина-Сан Жеора'
                              '\nА именно:'
                              '\nДля женщин: (10 × вес в килограммах) + (6,25 × рост в сантиметрах)'
                              ' − (5 × возраст в годах) − 161'
                              '\nДля мужчин: (10 × вес в килограммах) + (6,25 × рост в сантиметрах)'
                              ' − (5 × возраст в годах) + 5', reply_markup=ikb)
    await call.answer()


@dp.callback_query_handler(text='count')
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    print(data)
    await message.answer("Запускаем калькулятор, пожалуйста ожидайте")
    sleep(5)
    calories = (10*float(data['weight']))+(6.25*float(data['growth']))-(5*float(data['age']))-161
    await message.answer(f'Ваша суточная норма калорий: {int(calories)}. \nПриятного аппетита=)')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
