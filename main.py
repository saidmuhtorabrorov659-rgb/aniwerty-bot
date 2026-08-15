import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, ADMIN_ID, BOT_USERNAME
from database import init_db, get_anime

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Asosiy inline menyu tugmalari
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📺 Anime kodi orqali qidirish", callback_data="search_code")
            ],
            [
                InlineKeyboardButton(text="🔍 Anime nomi orqali qidirish", callback_data="search_name")
            ],
            [
                InlineKeyboardButton(text="🎭 Janr tanlash", callback_data="select_genre")
            ],
            [
                InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/aniwertyn1")
            ]
        ]
    )
    return keyboard

# /start xabari
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        anime_id = int(args[1])
        anime = await get_anime(anime_id)
        if anime:
            title, desc = anime
            await message.answer(f"🎬 <b>{title}</b>\n\n{desc}", parse_mode="HTML")
            return
        else:
            await message.answer("⚠️ Ushbu koddagi anime topilmadi.")
            return

    text = "👋 <b>Xush kelibsiz!</b>\n\nKerakli bo'limni tanlang yoki anime kodini yuboring 👇"
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="HTML")

# Tugmalar bosilgandagi javoblar
@dp.callback_query(lambda c: c.data == "search_code")
async def process_search_code(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("🔢 Anime kodini yuboring (Masalan: 1, 2, 3...):")

@dp.callback_query(lambda c: c.data == "search_name")
async def process_search_name(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("🔤 Anime nomini yozib yuboring:")

@dp.callback_query(lambda c: c.data == "select_genre")
async def process_select_genre(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("🎭 Janrlar ro'yxati tez orada qo'shiladi.")

# Kod orqali izlash
@dp.message()
async def code_handler(message: types.Message):
    if message.text and message.text.isdigit():
        anime_id = int(message.text)
        anime = await get_anime(anime_id)
        if anime:
            title, desc = anime
            await message.answer(f"🎬 <b>{title}</b>\n\n{desc}", parse_mode="HTML")
        else:
            await message.answer("⚠️ Ushbu koddagi anime topilmadi.")

# Render uchat soxta web server
async def handle(request):
    return web.Response(text="Bot ishlayapti!")

async def main():
    await init_db()
    
    # Web serverni ishga tushirish (Render o'chirib qo'ymasligi uchun)
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    
    print(f"@{BOT_USERNAME} muammosiz ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
