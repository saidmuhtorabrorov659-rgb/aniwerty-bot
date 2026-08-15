import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# =============================================================
# HANDLERLAR (Foydalanuvchi xabarlariga javob beruvchi qism)
# =============================================================

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📺 Anime kodi orqali qidirish")],
            [types.KeyboardButton(text="🔍 Anime nomi orqali qidirish")],
            [types.KeyboardButton(text="🎭 Janr tanlash")],
            [types.KeyboardButton(text="📢 Asosiy kanal")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "👋 Xush kelibsiz!\n\nKerakli bo'limni tanlang yoki anime kodini yuboring 👆",
        reply_markup=keyboard
    )

@dp.message(lambda msg: msg.text == "📺 Anime kodi orqali qidirish")
async def code_search(message: types.Message):
    await message.answer("134 Anime kodini yuboring (Masalan: 1, 2, 3...):")

@dp.message(lambda msg: msg.text == "🔍 Anime nomi orqali qidirish")
async def name_search(message: types.Message):
    await message.answer("abc Anime nomini yozib yuboring:")

@dp.message(lambda msg: msg.text == "🎭 Janr tanlash")
async def genre_select(message: types.Message):
    await message.answer("🎭 Janrlar ro'yxati tez orada qo'shiladi.")

@dp.message(lambda msg: msg.text == "📢 Asosiy kanal")
async def channel_link(message: types.Message):
    await message.answer("Kanalimizga a'zo bo'ling!")

# =============================================================
# RENDER WEB SERVER QISMI (Render o'chib qolmasligi uchun)
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
    # 1. Web serverni fonda yurgizish
    await start_web_server()
    
    # 2. Telegram bot pollingini boshlash
    print("@AniWerty_bot muammosiz ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
