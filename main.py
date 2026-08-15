import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# =============================================================
# OLDINGI INTERFEYS (INLINE TUGMALAR)
# =============================================================

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Oldingi chiroyli Inline menyu
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📺 Anime kodi orqali qidirish", callback_data="search_code")],
            [InlineKeyboardButton(text="🔍 Anime nomi orqali qidirish", callback_data="search_name")],
            [InlineKeyboardButton(text="🎭 Janr tanlash", callback_data="select_genre")],
            # Kanal havolasini o'zingizning kanalingiz havolasiga almashtiring
            [InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/aniwertyn1")]
        ]
    )
    await message.answer(
        "Kerakli bo'limni tanlang yoki anime kodini yuboring 👇",
        reply_markup=keyboard
    )

# Inline tugmalar bosilganda javob berish
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
# RENDER WEB SERVER QISMI
# =============================================================

async def handle(request):
    return web.Response(text="Bot running successfully!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await start_web_server()
    print("@AniWerty_bot muammosiz ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
