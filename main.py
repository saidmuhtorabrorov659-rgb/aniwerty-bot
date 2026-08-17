import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from config import BOT_TOKEN

# Render beradigan domen URL manzili
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://aniwerty-bot-2.onrender.com")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}{WEBHOOK_PATH}"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# =============================================================
# HANDLERLAR
# =============================================================

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📺 Anime kodi orqali qidirish", callback_data="search_code")],
            [InlineKeyboardButton(text="🔍 Anime nomi orqali qidirish", callback_data="search_name")],
            [InlineKeyboardButton(text="🎭 Janr tanlash", callback_data="select_genre")],
            [InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/KanalizingizNomi")]
        ]
    )
    await message.answer("Kerakli bo'limni tanlang yoki anime kodini yuboring 👇", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "search_code")
async def process_code(callback: types.CallbackQuery):
    await callback.message.answer("Anime kodini yuboring (Masalan: 1, 2, 3...):")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "search_name")
async def process_name(callback: types.CallbackQuery):
    await callback.message.answer("Anime nomini yozib yuboring:")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "select_genre")
async def process_genre(callback: types.CallbackQuery):
    await callback.message.answer("🎭 Janrlar ro'yxati tez orada qo'shiladi.")
    await callback.answer()

# =============================================================
# WEBHOOK SOZLAMASI
# =============================================================

async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

def main():
    dp.startup.register(on_startup)
    app = web.Application()
    
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    setup_application(app, dp, bot=bot)
    
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
