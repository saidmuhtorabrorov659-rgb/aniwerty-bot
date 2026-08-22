TOKEN = "8896707660:AAE9xXpaAD66t4ADpsVXflkL2QskIjdPBx4"  # <--- Yangi tokeningni shu yerga qo'shtirnoq ichiga tashlaysan

import logging
import sys
import os
import aiosqlite
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

DB_NAME = "aniwerty.db"

# Bazani yangilash uchun eskisini o'chiramiz
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
            # 1. Zombi 100
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (1, "Zombi 100", "Komediya, Ekshn"))
            zombi_eps = [
                "BAACAgIAAxkDAAO_aoMrWJrqEhmS6FrmDMmdP1UgeWAAAtkuAAIh-oBJoEzm5rYLpyg9BA",
                "BAACAgIAAxkDAAPAaoMrWNwYYARcEa-4NDygo9zwOLYAAjgyAAJGZyBKOYvpww2Wqu89BA",
                "BAACAgIAAxkDAAPBaoMrWKpeL_TdQ8fPnOSfDkJjWRAAAoItAAJ0qFhKPF6o7oaFIiA9BA",
                "BAACAgIAAxkDAAPCaoMrWPDNS-fiJhh3ZCDZOEWz74UAAts7AALTfeBKDD-6jImythI9BA",
                "BAACAgIAAxkDAAPDaoMrWDIAAVyYCgVp5IzlKqczn7UJAAL_MwACmTM4S2AoXyPKNBDrPQQ",
                "BAACAgIAAxkDAAPEaoMrWC494xPJnJ4mFunfszXBOOMAAp43AAKeybhLOjn6sYqZE0Q9BA",
                "BAACAgIAAxkDAAPFaoMrWDZcQ7xry1M-FCsDfRkK5gUAAqs0AALxLnlIQA1xqWBJPG09BA",
                "BAACAgIAAxkDAAPGaoMrWDPq0re9FfptyQRwOqHUx1AAArE0AALxLnlI3fXJzO3flk49BA",
                "BAACAgIAAxkDAAPHaoMrWCV3ZCJbkMZjPCC6srOHFhcAAvU9AAK8n5FIjtqGPUpNbuA9BA",
                "BAACAgIAAxkDAAPIaoMrWDg6OUZF1SRmu13HNIAOjf4AAq9CAAJ9wlFIL_Vc04HNKi09BA",
                "BAACAgIAAxkDAAPJaoMrWKqmMuZLE02W7t5IlCz6psMAAp5AAAJ-1WhImMLnoZob7cM9BA",
                "BAACAgIAAxkDAAPKaoMrWObCk_yw-wn2gB0AATmJ-vGnAAJyNwACmmKASIvYF4yXj8b9PQQ"
            ]
            for ep in zombi_eps:
                await db.execute("INSERT INTO episodes (anime_id, video_file_id) VALUES (?, ?)", (1, ep))

            # 2. Akademiyaning birinchi raqamli boy qizi
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (2, "Akademiyaning birinchi raqamli boy qizi", "Romantika"))
            akad_eps = [
                "BAACAgIAAxkDAAIBVmqG6uCIBQx6ZzcPotiUSZN-lPxCAAIapgAC51hoSjssBuD_2phrPQQ",
                "BAACAgIAAxkDAAIBV2qG6vI62sHwPoaZWI30u-65AAFNoAACapsAAjItoEoaVkHC4Zv7ED0E",
                "BAACAgIAAxkDAAIBWGqG6vZ3dtf7S9YdFLKmpjop49mDAAIErwAC38noSp0cgRXrYWllPQQ",
                "BAACAgIAAxkDAAIBWWqG6vuVr1X0Ygr3Wt2TmcXZAAEa0QACBKgAAhhdQUuGwUSkz1vu0z0E",
                "BAACAgIAAxkDAAIBWmqG6wSOq_hvZuPVA3c3oX2FjyE7AALoqgAC3C2AS5COMOI9-bHyPQQ",
                "BAACQAAxkBAAIBW2qG6wtI9O-ZDH0YTWDBTW0iTo3_AAJZHgACF6LoUz3imBALBhDOPQQ"
            ]
            for ep in akad_eps:
                await db.execute("INSERT INTO episodes (anime_id, video_file_id) VALUES (?, ?)", (2, ep))

            # 3. Arra Odam (Chainsaw Man)
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (3, "Arra Odam (Chainsaw Man)", "Ekshn, Qorong'u Fentezi, Shounen"))
            chainsaw_eps = [
                "BAACAgIAAxkDAAIB7mqJQdvtq0_8TqJX0MkL7PFL7zsYAAIDHwACXKNZs8JjwrjcGI_PQQ",
                "BAACAgIAAxkDAAIB72qJYXtAaYpxoqtecyI5JwAB7MdPpAgACfYMAA1t1YEu81jQzi6--ID0E",
                "BAACAgIAAxkDAAICWqJnunHnWC6RxmqAWiWyEX33asAAIEIgACLYgQSzoDERkp59oHPQQ",
                "BAACAgIAAxkDAAIC2qJnuzCir_Tqcc603qAQcskk95caAJyIgAcQNGgS0hxS1xKQdYVPQQ",
                "BAACAgIAAxkDAAICWqJnxH6rmNIQfsoB9qR0cN-vmhnAAK0IQACPaWBSwqr39AAAbW05D0E",
                "BAACAgIAAxkDAAICJ2qJnxcmlwXLARgTveGY0410YP2hAaAMEAAJE8flLmyi689aRjA9BA",
                "BAACAgIAAxkDAAICKWqJnxtfJgLeUKV61WTLuAAB_Oxx8wACgyMAAj50IEg_kp_3DD3dLTr0E",
                "BAACAgIAAxkDAAICK2qJnx9mUp34Qbk_z_RuJQyg1m2wAAIZKQAC3DaSvDSAiWvPGdPQQA",
                "BAACAgIAAxkDAAICLWqJnybZ6pEyCdqEerk32_y-WRyPAAiSNQAC3BAoSH26CMRr7plEPQQ",
                "BAACAgIAAxkDAAICL2qJnyo5a94Y0t4JJmBrp86hmIBTAAI2NQAC3BAoSFFJQNyPhI3PQQ",
                "BAACAgIAAxkDAAICMWqJny2ahrLKVfRkEP57reNZuDFIAAJENQAC3BAoS0AuMh1NiQxRPQQ",
                "BAACAgIAAxkDAAICWqJnYQJYUTipI3bcvscSBvCB_zVtnlAAAJWNQAIC3BAoSMnTmeaus90GPQQ",
                "BAACAgIAAxkDAAICNWqJnzcvGn80UUZCG9nm6_pLkxV-AAILkgAC80rRSegEI-Ds64PMPQQ"
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
    buttons = []
    for anime_id, title in rows:
        buttons.append([InlineKeyboardButton(text=title, callback_data=f"anime_{anime_id}")])
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
    keyboard = get_main_menu_keyboard()
    await message.answer(
        "👋 **Xush kelibsiz!** Kerakli bo'limni tanlang yoki anime kodini yuboring 👇",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

@dp.callback_query(F.data == "search_by_code")
async def search_code_cb(callback: types.CallbackQuery):
    keyboard = await get_anime_list_keyboard()
    await callback.message.edit_text("🎬 **Mavjud animelar ro'yxati:**", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
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
        await callback.message.answer_video(
            video=file_id,
            caption=f"🎬 **{title}** — {ep_number}-qism",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
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
    keyboard = get_main_menu_keyboard()
    try:
        await callback.message.edit_text(
            "👋 **Xush kelibsiz!** Kerakli bo'limni tanlang yoki anime kodini yuboring 👇",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        await callback.message.answer(
            "👋 **Xush kelibsiz!** Kerakli bo'limni tanlang yoki anime kodini yuboring 👇",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    await callback.answer()

if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
