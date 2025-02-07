import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from os import getenv
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = getenv('TOKEN')

black = "black.txt"

own = 565801111 #замените на ваш айди

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def kb_adm():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="Бан", callback_data='ban'),
        InlineKeyboardButton(text="Разбан", callback_data="unban")
    )
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="back"))
    return keyboard.as_markup()

def kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="Мой лс", url='https://t.me/CndCrime'), # замените на ваш лс
        InlineKeyboardButton(text="Информация", callback_data="info")
    )

    return keyboard.as_markup()

@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    if user_id not in black:
        await bot.send_message(
            chat_id=user_id,
            text='Здравствуй! Ты попал в бота для связи с @CndCrime! Отправь сообщение и жди ответа!', # тут тоже
            reply_markup=kb()
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text='Ой-ой. Походу вас заблокировали в боте!'
        )

@dp.message(Command("admin"))
async def admin(message: Message):
    user = message.from_user.id
    if user not in black:
        if user == own:
            await bot.send_message(
                chat_id=own,
                text='Выбирайте действие',
                reply_markup=kb_adm()
            )

@dp.callback_query(F.data == "info")
async def info(callback: types.CallbackQuery):
    user = callback.from_user.id
    if user not in black:
        await callback.message.edit_text(
            text='Бот создан с помощью @CndCrime. Вы можете получить исходник бесплатно!', # и тут
            reply_markup=callback.message.reply_markup
        )

@dp.callback_query(F.data == "ban")
async def ban_users(callback: types.CallbackQuery):
    await callback.message.edit_text(text='Введите айди для бана')
    ban_user = callback.message.text
    async with open(black, 'w') as bl:
        bl.write(ban_user+'\n')
    await callback.message.edit_text(text='Пользователь добавлен в черный лист!')

@dp.callback_query(F.data == "unban")
async def unbans(callback: types.CallbackQuery):
    await callback.message.edit_text(text='Введите айди для разбана')
    unban_user = callback.message.text
    async with open(black, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line for line in lines if unban_user not in line]
    async with open(black, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    await callback.message.edit_text(text='Пользователь удален из черного листа!')

@dp.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id == own:
        await callback.message.edit_text(text='Выбирайте действие', reply_markup=kb_adm())
    else:
        await callback.message.edit_text(
            text='Здравствуй! Ты попал в бота для связи с @CndCrime! Отправь сообщение и жди ответа!', # и туууут
            reply_markup=kb()
        )

message_links = {}

@dp.message(lambda message: message.text and message.from_user.id != own)
async def handle_text(message: Message):
    user = message.from_user.id
    if user not in black:
        await bot.send_message(own, f"|| Сообщение от пользователя {message.from_user.id} ||\n{message.text}")
        await message.answer("Ваше сообщение отправлено администратору, ожидайте ответа.")
    else:
        await bot.send_message('Ой-ой. Походу вас заблокировали в боте!')

@dp.message(lambda message: message.photo and message.from_user.id != own)
async def handle_photo(message: Message):
    user = message.from_user.id
    if user not in black:
        await bot.send_photo(own, message.photo[-1].file_id, caption=f"|| Сообщение от пользователя {message.from_user.id} ||")
        await message.answer("Ваше сообщение отправлено администратору, ожидайте ответа.")
    else:
        await bot.send_message('Ой-ой. Походу вас заблокировали в боте!')

@dp.message(lambda message: message.video and message.from_user.id != own)
async def handle_video(message: Message):
    user = message.from_user.id
    if user not in black:
        await bot.send_video(own, message.video.file_id, caption=f"|| Сообщение от пользователя {message.from_user.id} ||")
        await message.answer("Ваше сообщение отправлено администратору, ожидайте ответа.")
    else:
        await bot.send_message('Ой-ой. Походу вас заблокировали в боте!')

@dp.message(lambda message: message.from_user.id == own and message.reply_to_message)
async def admin_reply(message: Message):
    user_id = message.reply_to_message.text.split()[3]
    response = message.text
    await bot.send_message(user_id, f"Ответ от администратора:\n{response}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
