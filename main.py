TOKEN = "8896707660:AAHgKBY-Rv_oOQBc0eqBa194-TsUoWPcBKc"

import logging
import sys
import os
import aiosqlite
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

DB_NAME = "aniwerty.db"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_search_state = {}

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
            # 1-Anime: Zom 100 (start=1)
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (1, "Zombi 100: O'lim oldi ro'yxat", "🎬 Anime: Zombi 100: O'lim oldi ro'yxat\n🎥 Qismlar: 12\n💿 Sifati: 720p, 1080p\n🇺🇿 Tili: Uzbekcha\n🎭 Janr: Komediya, Ekshn, Sarguzasht\n🟢 Holati: Tugagan\n🆔 Anime Kodi: 1"))
            zombi_eps = [
                "BAACAgIAAxkBAAIDCGqLynGOtrxRW0NJvgVTbYclFoF6AALZLgACIfqASaBM5ua2C6coPQQ",
                "BAACAgIAAxkBAAIDCmqLynUJPQSlhazKQkTg3hVy8UXDAAI4MgACRmcgSjmL6cMNlqrvPQQ",
                "BAACAgIAAxkBAAIDDGqLyne6z4VONjWI5SpaT_BMPVeEAAKCLQACdKhYSjxeqO6GhSIgPQQ",
                "BAACAgIAAxkBAAIDDmqLynv_ddCoLw3ZS61oWc9aV3_dAALbOwAC033gSgw_uoyJsrYSPQQ",
                "BAACAgIAAxkBAAIDEGqLyn3iL9983B3S0BcKCad2bbQ_AAL_MwACmTM4S2AoXyPKNBDrPQQ",
                "BAACAgIAAxkBAAIDEmqLyoA0_K78Uqp0lJM1ReTgJr8HAAKeNwACnsm4Szo5-rGKmRNEPQQ",
                "BAACAgIAAxkBAAIDFGqLyoMq5s62Vdqv3lyjC6_7l4wmAAKrNAAC8S55SEANcalgSTxtPQQ",
                "BAACAgIAAxkBAAIDFmqLyoWto7g6N0pmj2izM4xbVOmHAAKxNAAC8S55SN31yczt35ZOPQQ",
                "BAACAgIAAxkBAAIDGGqLyog8MALKnaPZPrYzyERzz6dmAAL1PQACvJ-RSI7ahj1KTW7gPQQ",
                "BAACAgIAAxkBAAIDGmqLyop79sCilwJV0sLjam_5rBZlAAKvQgACfcJRSC_1XNOBzSotPQQ",
                "BAACAgIAAxkBAAIDHGqLyoz26ezhAzOAg5OdbCaJ3cfsAAKeQAACftVoSJjC56GaG-3DPQQ",
                "BAACAgIAAxkBAAIDHmqLyo87mMEd4tWcN3yCG_OL6QUMAAJyNwACmmKASIvYF4yXj8b9PQQ"
            ]
            for ep in zombi_eps:
                await db.execute("INSERT INTO episodes (anime_id, video_file_id) VALUES (?, ?)", (1, ep))

            # 2-Anime: Akademiyaning birinchi boy qizi (start=2)
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (2, "Akademiyaning birinchi raqamli boy qizi...", "🎬 Anime: Akademiyaning birinchi raqamli boy qiziga yashirincha enagalik qiladigan boʻldim\n🎥 Qismlar: 7\n💿 Sifati: 720p, 1080p\n🇺🇿 Tili: Uzbekcha\n🎭 Janr: Romantika, Komediya\n🟢 Holati: Tugagan\n🆔 Anime Kodi: 2"))
            akad_eps = [
                "BAACAgIAAxkBAAIC4GqLyYrO-0FrHTGykLAs7KdxBdJiAAIapgAC51hoSjssBuD_2phrPQQ",
                "BAACAgIAAxkBAAIC4mqLycyM-sC15Vtd_W1raHVeCGcZAAJqmwACMi2gShpWQcLhm_sQPQQ",
                "BAACAgIAAxkBAAIC5GqLydPFeYWMg9ON7MuTnyO8a1fAAAIErwAC38noSp0cgRXrYWllPQQ",
                "BAACAgIAAxkBAAIC5mqLydpioaX7H-3I_pMhYU7gZbtHAAIEqAACGF1BS4bBRKTPW-7TPQQ",
                "BAACAgIAAxkBAAIC6GqLyeA69H0Gy-XqJIy1qhAb1A_4AALoqgAC3C2AS5COMOI9-bHyPQQ",
                "BAACAgQAAxkBAAIC6mqLyeq6LnxIitI0s-W5S70YF5CsAAJZHgACF6LoUz3imBALBhDOPQQ",
                "BAACAgQAAxkBAAIC7GqLyfE5uR62XUnph9s0vPOilCpQAAKqHwACMnQxUEJkzEzWAAFTMz0E"
            ]
            for ep in akad_eps:
                await db.execute("INSERT INTO episodes (anime_id, video_file_id) VALUES (?, ?)", (2, ep))

            # 3-Anime: Arra Odam (start=3)
            await db.execute("INSERT INTO anime (id, title, description) VALUES (?, ?, ?)", 
                             (3, "Arra Odam (Chainsaw Man)", "🎬 Anime: Arra Odam (Chainsaw Man)\n🎥 Qismlar: 13\n💿 Sifati: 720p, 1080p\n🇺🇿 Tili: Uzbekcha\n🎭 Janr: Ekshn, Qorong'u Fentezi, Shounen\n🟢 Holati: Tugagan\n🆔 Anime Kodi: 3"))
            chainsaw_eps = [
                "BAACAgIAAxkBAAIC7mqLyixFAyBUE39aBieVXfRpNpOqAAIDHwACXKNZSs8JjwrjcGI_PQQ",
                "BAACAgIAAxkBAAIC72qLyizCmTaM7Ps3UkF2S5KZYj_VAAJ_IwACW3VgS7zWNDOLr76IPQQ",
                "BAACAgIAAxkBAAIC8GqLyixlTUmT_3DwyD1Fr0EfNGC5AAIEIgAClYgQSzoDERkp59oHPQQ",
                "BAACAgIAAxkBAAIC8WqLyiwwEBs1VEQoP68TMs4vlEHpAAJyIgACqNGgS0hxSlxKQdYVPQQ",
                "BAACAgIAAxkBAAIC8mqLyixxvjV_10NALdYfGsfgA92HAAK0IQACPaWBSwqr39AAAbWO5D0E",
                "BAACAgIAAxkBAAIC82qLyiwNWqdOR2YN0Mf4vNRAA8_aAAMeAAJE8flLmyi689aR8jA9BA",
                "BAACAgIAAxkBAAIC9GqLyizdocOXHHSEJu2uupJTfP8zAAKDIwACPnQgSD-Sn_cMPd0tPQQ",
                "BAACAgIAAxkBAAIC9WqLyiwSJb5-eAZq0IDHnjCwG2QbAAIZKQAC3TdASvDSAiWwvPGdPQQ",
                "BAACAgIAAxkBAAIC72qLyizCmTaM7Ps3UkF2S5KZYj_VAAJ_IwACW3VgS7zWNDOLr76IPQQ",
                "BAACAgIAAxkBAAIC92qLyiwqdn7YgZ6Py1lUygLjEWA6AAI2NQAC3BAoSFFJQNyPhiX3PQQ",
                "BAACAgIAAxkBAAIC-GqLyixg71LdhiIESoBszbBgPb3RAAJENQAC3BAoSOauMhlNiQxRPQQ",
                "BAACAgIAAxkBAAIC-WqLyiz9uKJawHP0mOfQtIkIkfVzAAJWNQAC3BAoSMnTmeaus9OGPQQ",
                "BAACAgIAAxkBAAIC-mqLyix7aHfYULgb1Ff8yYETGHUaAAIlkgAC80rRSegEI-Ds64PMPQQ"
            ]
            for ep in chainsaw_eps:
                await db.execute("INSERT INTO episodes (anime_id, video_file_id) VALUES (?, ?)", (3, ep))

            await db.commit()

def get_main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📺 Anime kodi orqali qidirish", callback_data="search_by_code")],
        [InlineKeyboardButton(text="🔍 Anime nomi orqali qidirish", callback_data="search_by_name")],
        [InlineKeyboardButton(text="🎭 Janr tanlash", callback_data="choose_genre")],
        [InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/aniwertyn1")]
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
    user_search_state.pop(message.from_user.id, None)
    
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        anime_id = int(args[1])
        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute("SELECT description FROM anime WHERE id = ?", (anime_id,)) as cursor:
                anime = await cursor.fetchone()
        if anime:
            description = anime[0]
            keyboard = await get_episodes_keyboard(anime_id)
            await message.answer(f"{description}\n\n👇 Qismni tanlang:", reply_markup=keyboard)
            return

    await message.answer(
        "👋 **Xush kelibsiz!** Kerakli bo'limni tanlang yoki anime kodini yuboring 👇",
        reply_markup=get_main_menu_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

@dp.callback_query(F.data == "search_by_code")
async def search_code_cb(callback: types.CallbackQuery):
    user_search_state.pop(callback.from_user.id, None)
    keyboard = await get_anime_list_keyboard()
    await callback.message.edit_text("🎬 **Mavjud animelar ro'yxati (yoki kodini yuboring):**", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    await callback.answer()

@dp.callback_query(F.data == "search_by_name")
async def search_name_cb(callback: types.CallbackQuery):
    user_search_state[callback.from_user.id] = "waiting_for_name"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")]])
    await callback.message.edit_text("🔍 Anime nomini yuboring:", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    await callback.answer()

@dp.callback_query(F.data == "choose_genre")
async def genre_cb(callback: types.CallbackQuery):
    user_search_state.pop(callback.from_user.id, None)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")]])
    await callback.message.edit_text("🎭 Janrni tanlang:", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    await callback.answer()

@dp.message(F.text)
async def handle_text_messages(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip()

    if user_search_state.get(user_id) == "waiting_for_name":
        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute("SELECT id, description FROM anime WHERE title LIKE ?", (f"%{text}%",)) as cursor:
                results = await cursor.fetchall()
        
        if results:
            for anime_id, description in results:
                keyboard = await get_episodes_keyboard(anime_id)
                await message.answer(f"{description}\n\n👇 Qismni tanlang:", reply_markup=keyboard)
            user_search_state.pop(user_id, None)
        else:
            await message.answer("⚠️ Bunday nomdagi anime topilmadi!")
        return

    if text.isdigit():
        anime_id = int(text)
        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute("SELECT description FROM anime WHERE id = ?", (anime_id,)) as cursor:
                anime = await cursor.fetchone()
                
        if anime:
            description = anime[0]
            keyboard = await get_episodes_keyboard(anime_id)
            await message.answer(f"{description}\n\n👇 Qismni tanlang:", reply_markup=keyboard)
        else:
            await message.answer("⚠️ Bunday kodli anime topilmadi!")
    else:
        await message.answer("❓ Noma'lum buyruq. /start ni bosing.")

@dp.callback_query(F.data.startswith("anime_"))
async def show_anime(callback: types.CallbackQuery):
    anime_id = int(callback.data.split("_")[1])
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT description FROM anime WHERE id = ?", (anime_id,)) as cursor:
            anime = await cursor.fetchone()
    if anime:
        description = anime[0]
        keyboard = await get_episodes_keyboard(anime_id)
        try:
            await callback.message.edit_text(f"{description}\n\n👇 Qismni tanlang:", reply_markup=keyboard)
        except Exception:
            await callback.message.answer(f"{description}\n\n👇 Qismni tanlang:", reply_markup=keyboard)
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
            await callback.answer("⚠️ Video yuborishda xatolik!", show_alert=True)
    else:
        await callback.answer("⚠️ Qism topilmadi!", show_alert=True)
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
    user_search_state.pop(callback.from_user.id, None)
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

if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
    @dp.message(F.video)
async def handle_videos(message: types.Message):
    file_id = message.video.file_id
    await message.answer(f"📹 **Video qabul qilindi!**\n\nUshbu videoning `file_id` si:\n`{file_id}`", parse_mode=ParseMode.MARKDOWN)
