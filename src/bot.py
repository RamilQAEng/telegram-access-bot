import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv(os.path.join(os.path.dirname(__file__), '../config/.env'))

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

REQUIRED_CHANNELS = list(map(int, os.getenv("CHANNELS").split(','))) if os.getenv("CHANNELS") else []

async def check_subscription(user_id: int) -> bool:
    """Проверка подписки на все обязательные каналы"""
    for channel_id in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            logging.error(f"Ошибка проверки подписки на канал {channel_id}: {e}")
            continue
    return True

async def get_channels_keyboard():
    """Создание клавиатуры с кнопками для подписки на каналы"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])  # Инициализируем с пустым списком кнопок
    for channel_id in REQUIRED_CHANNELS:
        try:
            chat = await bot.get_chat(channel_id)
            button = InlineKeyboardButton(
                text=f"Подписаться на {chat.title}", 
                url=chat.invite_link
            )
            keyboard.inline_keyboard.append([button])  # Добавляем кнопку в клавиатуру
        except Exception as e:
            logging.error(f"Ошибка получения информации о канале {channel_id}: {e}")
    
    # Добавляем кнопку для проверки подписки
    check_button = InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")
    keyboard.inline_keyboard.append([check_button])
    
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if await check_subscription(message.from_user.id):
        # Меню с навигацией
        await message.answer(
            "Доступ разрешен! Выберите раздел:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Раздел 1", callback_data="section_1")],
                [InlineKeyboardButton(text="Раздел 2", callback_data="section_2")],
            ])
        )
    else:
        # Если доступ запрещен
        await message.answer(
            "❌ Подпишитесь на каналы:",
            reply_markup=await get_channels_keyboard()
        )

@dp.callback_query(F.data.startswith("section_"))
async def handle_section(callback: types.CallbackQuery):
    section = callback.data.split("_")[1]
    if section == "1":
        await callback.message.answer("Вы выбрали Раздел 1. Вот материалы: ...")
    elif section == "2":
        await callback.message.answer("Вы выбрали Раздел 2. Вот материалы: ...")

async def on_startup(bot: Bot):
    """Проверка доступности каналов при старте"""
    for channel_id in REQUIRED_CHANNELS:
        try:
            chat = await bot.get_chat(channel_id)
            logging.info(f"Канал доступен: {chat.title} (ID: {channel_id})")
        except Exception as e:
            logging.error(f"Канал недоступен (ID: {channel_id}): {e}")

if __name__ == '__main__':
    dp.startup.register(on_startup)
    dp.run_polling(bot)