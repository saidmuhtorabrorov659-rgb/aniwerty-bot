import logging
import sys
import aiosqlite
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import DB_NAME, init_db, get_anime

TOKEN = "8896707660:AAGZ7CpCTVXhiDJFfcycOT_YRyFvC3wU5RE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Asosiy menyu tugmalari (animelarni bazadan chiqarish uchun)
async def get_main_keyboard():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT id, title FROM anime") as cursor:
            rows = await cursor.fetchall()
            
    buttons = []
    for anime_id, title in rows:
        buttons.append([InlineKeyboardButton(text=title, callback_data=f"anime_{anime_id}")])
        
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Qismlar tugmalarini bazadan olish
async def get_episodes_keyboard(anime_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT id FROM episodes WHERE anime_id = ?", (anime_id,)) as cursor:
            episodes = await cursor.fetchall()
            
    buttons = []
    row = []
    # Qismlarni tartib bilan chiqarish
    for idx, (ep_db_id,) in enumerate(episodes, start=1):
        row.append(InlineKeyboardButton(text=str(idx), callback_data=f"ep_{anime_id}_{ep_db_id}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
        
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    # Bot ishga tushganda bazani tekshirib yaratib qo'yadi
    await init_db()
    
    keyboard = await get_main_keyboard()
    await message.answer(
        "👋 **Xush kelibsiz!**\nKerakli animeni tanlang:",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

@dp.callback_query(F.data.startswith("anime_"))
async def show_anime(callback: types.CallbackQuery):
    anime_id = int(callback.data.split("_")[1])
    
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT title, description FROM anime WHERE id = ?", (anime_id,)) as cursor:
            anime = await cursor.fetchone()
            
    if anime:
        title, description = anime
        text = f"🎬 **{title}**\n\n📌 **Tavsif:** {description or 'Mavjud emas'}\n\nQismni tanlang:"
        keyboard = await get_episodes_keyboard(anime_id)
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    else:
        await callback.answer("⚠️ Anime topilmadi!", show_alert=True)
        
    await callback.answer()

@dp.callback_query(F.data.startswith("ep_"))
async def send_episode(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    anime_id = parts[1]
    ep_db_id = parts[2]
    
    async with aiosqlite.connect(DB_NAME) as db:
        # Video file_id ni va anime nomini olish
        async with db.execute("SELECT video_file_id FROM episodes WHERE id = ?", (ep_db_id,)) as cursor:
            ep_data = await cursor.fetchone()
            
        async with db.execute("SELECT title FROM anime WHERE id = ?", (anime_id,)) as cursor:
            anime_data = await cursor.fetchone()

    if ep_data and anime_data:
        file_id = ep_data[0]
        title = anime_data[0]
        keyboard = await get_episodes_keyboard(int(anime_id))
        
        await callback.message.answer_video(
            video=file_id,
            caption=f"🎬 {title}",
            reply_markup=keyboard
        )
    else:
        await callback.answer("⚠️ Bu qism topilmadi!", show_alert=True)
        
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    keyboard = await get_main_keyboard()
    await callback.message.edit_text(
        "👋 **Xush kelibsiz!**\nKerakli animeni tanlang:",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    await callback.answer()

if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
