TOKEN = "8896707660:AAH3jUQq0K1SnsmrmEsEgUOW__PilNtMDGw"

import logging
import sys
import os
import aiosqlite
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

DB_NAME = "aniwerty.db"

# Eski bazani tozalab, noldan boshlash uchun
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS anime (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anime_id INTEGER,
                video_file_id TEXT,
                FOREIGN KEY (anime_id) REFERENCES anime (id)
            )
        """)
        await db.commit()
        
        async with db.execute("SELECT COUNT(*) FROM anime") as cursor:
            count = (await cursor.fetchone())[0]
            
        if count == 0:
            # 1-Anime: Zombi 100
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (1, "Zombi 100", "Komediya, Ekshn"))
            zombi_eps = [
                "BURE_FILE_ID_1", "BURE_FILE_ID_2"
            ]
            for ep in zombi_eps:
                await db.execute("INSERT INTO episodes (anime_id, video_file_id) VALUES (?, ?)", (1, ep))

            # 2-Anime: Akademiyaning birinchi raqamli boy qizi
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (2, "Akademiyaning birinchi raqamli boy qizi", "Romantika"))
            akad_eps = [
                "BURE_FILE_ID_1", "BURE_FILE_ID_2"
            ]
            for ep in akad_eps:
                await db.execute("INSERT INTO episodes (anime_id, video_file_id) VALUES (?, ?)", (2, ep))

            # 3-Anime: Arra Odam (Chainsaw Man)
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (3, "Arra Odam (Chainsaw Man)", "Ekshn, Qorong'u Fentezi, Shounen"))
            chainsaw_eps = [
                "BURE_FILE_ID_1", "BURE_FILE_ID_2"
            ]
            for ep in chainsaw_eps:
                await db.execute("INSERT INTO episodes (anime_id, video_file_id) VALUES (?, ?)", (3, ep))

            await db.commit()

# Asosiy menyu tugmalari
def get_main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📺 Anime kodi orqali qidirish", callback_data="search_by_code")],
        [InlineKeyboardButton(text="🔍 Anime nomi orqali qidirish", callback_data="search_by_name")],
        [InlineKeyboardButton(text="🎭 Janr tanlash", callback_data="choose_genre")],
        [InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/A_ToolsX")]
    ])

async def get_anime_list_keyboard():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT id, title FROM anime") as cursor:
            rows = await cursor.fetchall()
    buttons = [[InlineKeyboardButton(text=f"{anime_id}. {title}", callback_data=f"anime_{anime_id}")] for anime_id, title in rows]
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def get_episodes_keyboard(anime_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT id FROM episodes WHERE anime_id = ?", (anime_id,)) as cursor:
            episodes = await cursor.fetchall()
    buttons = []
    row = []
    for idx, (ep_db_id,) in enumerate(episodes, start=1):
        row.append(InlineKeyboardButton(text=str(idx), callback_data=f"ep_{anime_id}_{ep_db_id}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_list")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await init_db()
    await message.answer(
        "👋 **Xush kelibsiz!** Kerakli bo'limni tanlang yoki anime kodini (masalan: 1, 2, 3) yuboring 👇",
        reply_markup=get_main_menu_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

# Foydalanuvchi raqam (ID) yuborganda qidirish
@dp.message(F.text.regexp(r"^\d+$"))
async def search_by_code_message(message: types.Message):
    anime_id = int(message.text)
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT title, description FROM anime WHERE id = ?", (anime_id,)) as cursor:
            anime = await cursor.fetchone()
            
    if anime:
        title, description = anime
        text = f"🎬 **{title}**\n\n📌 **Tavsif:** {description}\n\nQismni tanlang:"
        keyboard = await get_episodes_keyboard(anime_id)
        await message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("⚠️ Bunday kodli anime topilmadi! Qaytadan urinib ko'ring.")

@dp.callback_query(F.data == "search_by_code")
async def search_code_cb(callback: types.CallbackQuery):
    keyboard = await get_anime_list_keyboard()
    await callback.message.edit_text("🎬 **Mavjud animelar ro'yxati (yoki kodini yuboring):**", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    await callback.answer()

@dp.callback_query(F.data == "search_by_name")
async def search_name_cb(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")]])
    await callback.message.edit_text("🔍 Anime nomini yuboring:", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    await callback.answer()

@dp.callback_query(F.data == "choose_genre")
async def genre_cb(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")]])
    await callback.message.edit_text("🎭 Janrni tanlang:", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    await callback.answer()

@dp.callback_query(F.data.startswith("anime_"))
async def show_anime(callback: types.CallbackQuery):
    anime_id = int(callback.data.split("_")[1])
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT title, description FROM anime WHERE id = ?", (anime_id,)) as cursor:
            anime = await cursor.fetchone()
    if anime:
        title, description = anime
        text = f"🎬 **{title}**\n\n📌 **Tavsif:** {description}\n\nQismni tanlang:"
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
        async with db.execute("SELECT video_file_id FROM episodes WHERE id = ?", (ep_db_id,)) as cursor:
            ep_data = await cursor.fetchone()
        async with db.execute("SELECT title FROM anime WHERE id = ?", (anime_id,)) as cursor:
            anime_data = await cursor.fetchone()
        async with db.execute("SELECT id FROM episodes WHERE anime_id = ?", (anime_id,)) as cursor:
            all_eps = await cursor.fetchall()

    ep_number = "1"
    for idx, (db_id,) in enumerate(all_eps, start=1):
        if str(db_id) == str(ep_db_id):
            ep_number = str(idx)
            break

    if ep_data and anime_data:
        file_id = ep_data[0]
        title = anime_data[0]
        keyboard = await get_episodes_keyboard(int(anime_id))
        try:
            await callback.message.answer_video(
                video=file_id,
                caption=f"🎬 **{title}** — {ep_number}-qism",
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception:
            await callback.answer("⚠️ Bu qism uchun video yuklanmagan yoki file_id yaroqsiz!", show_alert=True)
    else:
        await callback.answer("⚠️ Bu qism topilmadi!", show_alert=True)
    await callback.answer()

@dp.callback_query(F.data == "back_to_list")
async def back_to_list(callback: types.CallbackQuery):
    keyboard = await get_anime_list_keyboard()
    try:
        await callback.message.edit_text("🎬 **Mavjud animelar ro'yxati:**", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    except Exception:
        await callback.message.answer("🎬 **Mavjud animelar ro'yxati:**", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(
            "👋 **Xush kelibsiz!** Kerakli bo'limni tanlang yoki anime kodini yuboring 👇",
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        await callback.message.answer(
            "👋 **Xush kelibsiz!** Kerakli bo'limni tanlang yoki anime kodini yuboring 👇",
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    await callback.answer()

# Botga istalgan video tashlanganda uning file_id sini chiqarib beradi
@dp.message(F.video)
async def get_file_id(message: types.Message):
    file_id = message.video.file_id
    await message.reply(f"📹 **Video File ID:**\n\n`{file_id}`", parse_mode=ParseMode.MARKDOWN)

if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
