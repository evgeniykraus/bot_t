import re

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

import controller
from conn import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b_menu = KeyboardButton('ℹ Показать меню')
kb.add(b_menu)


class Form(StatesGroup):
    user_input = State()
    dell_sub = State()
    add_sub = State()


def is_valid(user_input):
    result = re.match("^[А-я]{1,15} [А-я]{1,15} [А-я]{1,15} ((\+7|7|8)+([0-9]){10})$", user_input) is not None
    if not result and len(user_input) <= 12:
        return False
    else:
        return result


def show_subs(array):
    subscriber_list = ''
    count = 1
    for value in array:
        temp = value.split(' ')
        subscriber_list += f'<b>Контакт # {count}</b>\n<b>ФИО:</b> {temp[0]} {temp[1]} {temp[2]}\n<b>Телефон:</b> +{temp[3]}\n\n'
        count += 1
    return subscriber_list


def start_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)

    ibf1 = InlineKeyboardButton(callback_data='subscriber_list',
                                text='📖️ Список контактов')
    ibf2 = InlineKeyboardButton(callback_data='search_subscriber',
                                text='🔎 Поиск контакта')

    keyboard.add(ibf1, ibf2)

    return keyboard


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Привет, {message.from_user.full_name}!',
                           parse_mode='HTML',
                           reply_markup=kb)


@dp.message_handler(text='ℹ Показать меню', state=None)
async def get_menu(message: types.Message):
    keyboard = start_menu()

    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<b>Главное меню</b>',
                           parse_mode='HTML',
                           reply_markup=keyboard)


@dp.callback_query_handler(text='show_start_menu')
async def get_start_menu(callback: types.CallbackQuery):
    keyboard = start_menu()

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f'<b>Главное меню</b>',
                           parse_mode='HTML',
                           reply_markup=keyboard)


@dp.callback_query_handler(text='search_subscriber')
async def get_subs_list_callback(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)

    ib1 = InlineKeyboardButton(callback_data='cancel_search',
                               text='Назад')

    keyboard.add(ib1)

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f'<b>Поиск контакта</b>\n<i>Введите ФИО '
                                f'контакта или номер телефона для поиска</i>',
                           parse_mode='HTML',
                           reply_markup=keyboard)
    await Form.user_input.set()


@dp.message_handler(state=Form.user_input)
async def find_subscriber(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)

    ib1 = InlineKeyboardButton(callback_data='search_subscriber',
                               text='Повторить поиск')

    ib2 = InlineKeyboardButton(callback_data='show_start_menu',
                               text='Главное меню')

    keyboard.add(ib1, ib2)
    async with state.proxy() as proxy:
        proxy['user_input'] = message.text
        result = controller.get_subscriber_data(proxy['user_input'])

        subscriber_list = show_subs(result)

        if subscriber_list:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'{subscriber_list}\n',
                                   parse_mode='HTML',
                                   reply_markup=keyboard)
            await state.finish()
        elif proxy['user_input'] == 'ℹ Показать меню':
            keyboard = start_menu()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Главное меню</b>',
                                   parse_mode='HTML',
                                   reply_markup=keyboard)
            await state.finish()
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'Я ничего не нашел!',
                                   parse_mode='HTML',
                                   reply_markup=keyboard)
            await state.finish()


@dp.callback_query_handler(text='cancel_search', state=Form.user_input)
async def get_start_menu(callback: types.CallbackQuery, state: FSMContext):
    keyboard = start_menu()

    await callback.message.edit_text(text=f'<b>Главное меню</b>',
                                     parse_mode='HTML',
                                     reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(text='cancel_search', state=Form.add_sub)
async def get_start_menu(callback: types.CallbackQuery, state: FSMContext):
    keyboard = start_menu()

    await callback.message.edit_text(text=f'<b>Главное меню</b>',
                                     parse_mode='HTML',
                                     reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(text='subscriber_list')
async def get_subs_list_callback(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)

    ib1 = InlineKeyboardButton(callback_data='show_start_menu',
                               text='Назад')
    ib2 = InlineKeyboardButton(callback_data='add_contact',
                               text='Добавить контакт')
    ib3 = InlineKeyboardButton(callback_data='dell_contact',
                               text='Удалить контакт')

    keyboard.add(ib2, ib3, ib1)
    subscriber_list = show_subs(controller.get_all_subscribers())

    await callback.message.edit_text(f'{subscriber_list}\n',
                                     parse_mode='HTML',
                                     reply_markup=keyboard)


@dp.callback_query_handler(text='cancel_search', state=Form.dell_sub)
async def get_start_menu(callback: types.CallbackQuery, state: FSMContext):
    keyboard = start_menu()

    await callback.message.edit_text(text=f'<b>Главное меню</b>',
                                     parse_mode='HTML',
                                     reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(text='add_contact')
async def add_sub_callback(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)

    ib1 = InlineKeyboardButton(callback_data='cancel_search',
                               text='Отмена')

    keyboard.add(ib1)
    await Form.add_sub.set()
    await callback.message.edit_text(f'<b>Добавление контакта</b>\n<i>Введите ФИО '
                                     f'контакта и номер телефона через пробел</i>\n'
                                     f'<b>Пример:</b> Иванов Иван Иванович +79998887766',
                                     parse_mode='HTML',
                                     reply_markup=keyboard)


@dp.message_handler(state=Form.add_sub)
async def add_subscriber(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)

    ib1 = InlineKeyboardButton(callback_data='add_contact',
                               text='Повторить ввод')

    ib2 = InlineKeyboardButton(callback_data='show_start_menu',
                               text='Главное меню')

    keyboard.add(ib1, ib2)

    async with state.proxy():
        new_subscriber = message.text

        if not is_valid(new_subscriber):
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Ошибка ввода!</b>\n<i>Введите ФИО '
                                        f'контакта и номер телефона через пробел</i>\n'
                                        f'<b>Пример:</b> Иванов Иван Иванович 79998887766',
                                   parse_mode='HTML',
                                   reply_markup=keyboard)
            await state.finish()
        else:
            result = controller.add_new_sub(new_subscriber)
            if result == -1:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f'<b>Ошибка!</b>\n'
                                            f'Номер телефона уже есть в базе',
                                       parse_mode='HTML',
                                       reply_markup=keyboard)
                await state.finish()
            else:
                new_subscriber = new_subscriber.split(" ")
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f'<b>Готово!</b>\n'
                                            f'{new_subscriber[0]} {new_subscriber[1]} добавлен в базу',
                                       parse_mode='HTML',
                                       reply_markup=keyboard)
                await state.finish()


@dp.callback_query_handler(text='dell_contact')
async def dell_sub_callback(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)

    ib1 = InlineKeyboardButton(callback_data='cancel_search',
                               text='Отмена')

    keyboard.add(ib1)
    await Form.dell_sub.set()
    await bot.send_message(chat_id=callback.from_user.id,
                           text=f'<b>Удаление контакта</b>\n<i>Введите номер телефона контакта, который хотите удалить</i>',
                           parse_mode='HTML',
                           reply_markup=keyboard)


@dp.message_handler(state=Form.dell_sub)
async def add_subscriber(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)

    ib1 = InlineKeyboardButton(callback_data='dell_contact',
                               text='Повторить ввод')

    ib2 = InlineKeyboardButton(callback_data='show_start_menu',
                               text='Главное меню')

    keyboard.add(ib1, ib2)

    async with state.proxy():
        res = controller.phone_number(message.text)
        result = re.sub(r"^\+", "", message.text)
        result = re.sub(r"^8", "7", result)
        if res == -1:
            controller.dell_sub(result)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Готово!</b>\n'
                                        f'Контакт с номером <b>{result}</b> был удален',
                                   parse_mode='HTML',
                                   reply_markup=keyboard)
            await state.finish()
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Ошибка ввода!</b>\n'
                                        f'Контакт с номером телефона <b>{message.text}</b> не найден в базе',
                                   parse_mode='HTML',
                                   reply_markup=keyboard)
            await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
