import asyncio
import json
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 2049374426
CHANNEL_URL = "https://t.me/aniwertyn1" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

def load_db():
    if os.path.exists("anime_db.json"):
        with open("anime_db.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Asosiy Kanalimiz", url=CHANNEL_URL)],
            [
                InlineKeyboardButton(text="📚 Barcha Animelar", callback_data="catalog"),
                InlineKeyboardButton(text="🎭 Janrlar", callback_data="genres_menu")
            ],
            [InlineKeyboardButton(text="🔍 Qidiruv Bo'yicha Yordam", callback_data="help_search")]
        ]
    )

def make_episodes_keyboard(anime_code, season_num, seasons):
    episodes = seasons.get(str(season_num), {})
    buttons = []
    row = []
    
    # Qismlar tugmalarini chiqarish (har qatorda 4 tadan)
    for ep_num in episodes.keys():
        row.append(InlineKeyboardButton(
            text=f"{ep_num}-qism", 
            callback_data=f"ep:{anime_code}:{season_num}:{ep_num}"
        ))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    # Keyingi / Oldingi fasl tugmalari
    nav_row = []
    prev_season = str(int(season_num) - 1)
    next_season = str(int(season_num) + 1)

    if prev_season in seasons:
        nav_row.append(InlineKeyboardButton(
            text=f"⏪ {prev_season}-faslga o'tish", 
            callback_data=f"season:{anime_code}:{prev_season}"
        ))
    if next_season in seasons:
        nav_row.append(InlineKeyboardButton(
            text=f"⏩ {next_season}-faslga o'tish", 
            callback_data=f"season:{anime_code}:{next_season}"
        ))
    
    if nav_row:
        buttons.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@dp.message(F.video | F.document)
async def get_file_id(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⚠️ Botga video yuklash faqat administrator uchun ruxsat etilgan.")
        return

    file_id = message.video.file_id if message.video else message.document.file_id
    file_type = "Video" if message.video else "Hujjat (Document)"

    await message.answer(
        f"👑 <b>Admin rejimi: {file_type} qabul qilindi!</b>\n\n"
        f"🔑 <b>Nusxalab olish uchun file_id:</b>\n"
        f"<code>{file_id}</code>",
        parse_mode=ParseMode.HTML
    )


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        f"Salom, {message.from_user.first_name}! 👋\n\n"
        f"<b>AniWerty</b> rasmiy botiga xush kelibsiz!\n"
        f"Bizning kanalimizga a'zo bo'ling va eng sara animelarni tomosha qiling.\n\n"
        f"👇 Kerakli bo'limni tanlang yoki anime <b>kodi/nomini</b> yuboring:",
        reply_markup=main_menu(),
        parse_mode=ParseMode.HTML
    )


@dp.callback_query(F.data == "catalog")
async def show_catalog(call: types.CallbackQuery):
    db = load_db()
    if not db:
        await call.message.edit_text("Hozircha bazada animelar yo'q.", reply_markup=main_menu())
        return

    text = "📚 <b>Mavjud Animelar Katalogi:</b>\n\n"
    for code, data in db.items():
        seasons = data.get("seasons", {})
        total_seasons = len(seasons)
        total_episodes = sum(len(ep) for ep in seasons.values())
        
        text += f"🔹 <b>Kodi: {code}</b> — {data['title']} ({total_seasons} ta fasl, {total_episodes} ta qism)\n"
    
    text += "\nKo'rmoqchi bo'lgan animenangiz kodini chatga yuboring!"
    await call.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=main_menu())


@dp.callback_query(F.data == "genres_menu")
async def show_genres(call: types.CallbackQuery):
    db = load_db()
    genres_set = set()
    for anime in db.values():
        for genre in anime.get("genres", []):
            genres_set.add(genre)

    if not genres_set:
        await call.answer("Hozircha janrlar kiritilmagan!", show_alert=True)
        return

    buttons = []
    row = []
    for g in sorted(genres_set):
        row.append(InlineKeyboardButton(text=f"🎭 {g}", callback_data=f"genre:{g}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
        
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_main")])
    await call.message.edit_text("🎭 <b>O'zingizga yoqqan janrni tanlang:</b>", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode=ParseMode.HTML)


@dp.callback_query(F.data.startswith("genre:"))
async def filter_by_genre(call: types.CallbackQuery):
    selected_genre = call.data.split(":")[1]
    db = load_db()

    results = [f"🔹 <b>Kodi: {code}</b> — {data['title']}" for code, data in db.items() if selected_genre in data.get("genres", [])]

    if results:
        text = f"🎭 <b>'{selected_genre}' janridagi animelar:</b>\n\n" + "\n".join(results) + "\n\nKerakli anime kodini chatga yuboring!"
    else:
        text = "Ushbu janrda hali animelar yo'q."

    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Janrlarga qaytish", callback_data="genres_menu")]])
    await call.message.edit_text(text, reply_markup=kb, parse_mode=ParseMode.HTML)


@dp.callback_query(F.data == "back_main")
async def back_to_main(call: types.CallbackQuery):
    await call.message.edit_text("<b>AniWerty</b> asosiy menyusi:\nKerakli bo'limni tanlang:", reply_markup=main_menu(), parse_mode=ParseMode.HTML)


@dp.callback_query(F.data == "help_search")
async def help_search(call: types.CallbackQuery):
    await call.answer("Qidirish usullari:\n1. Kod yuboring (masalan: 1, 2)\n2. Nomini yozing (masalan: Solo Leveling)\n3. Janrlardan tanlang!", show_alert=True)


@dp.message(F.text)
async def handle_text_search(message: types.Message):
    query = message.text.strip()
    db = load_db()

    if query in db:
        anime = db[query]
        seasons = anime.get("seasons", {})
        
        kb = make_episodes_keyboard(query, "1", seasons)

        await message.answer(
            f"{anime['description']}\n\n"
            f"🎬 <b>1-fasl qismlaridan birini tanlang:</b>",
            reply_markup=kb,
            parse_mode=ParseMode.HTML
        )
        return

    results = [f"🔹 <b>Kodi: {code}</b> — {data['title']}" for code, data in db.items() if query.lower() in data["title"].lower()]

    if results:
        response_text = f"🔍 <b>'{query}' bo'yicha topilgan animelar:</b>\n\n" + "\n".join(results) + "\n\nKerakli anime kodini chatga yuboring!"
        await message.answer(response_text, parse_mode=ParseMode.HTML)
    else:
        await message.answer("❌ Hech narsa topilmadi. Kod yoki nomni to'g'ri kiritganingizga ishonch hosil qiling.")


@dp.callback_query(F.data.startswith("season:"))
async def change_season(call: types.CallbackQuery):
    _, anime_code, target_season = call.data.split(":")
    db = load_db()
    anime = db.get(anime_code)
    
    if anime:
        seasons = anime.get("seasons", {})
        kb = make_episodes_keyboard(anime_code, target_season, seasons)
        await call.message.edit_text(
            f"{anime['description']}\n\n"
            f"🎬 <b>{target_season}-fasl qismlaridan birini tanlang:</b>",
            reply_markup=kb,
            parse_mode=ParseMode.HTML
        )
        await call.answer()


@dp.callback_query(F.data.startswith("ep:"))
async def send_episode(call: types.CallbackQuery):
    _, anime_code, season_num, ep_num = call.data.split(":")
    db = load_db()
    
    anime = db.get(anime_code)
    if anime and season_num in anime.get("seasons", {}):
        file_id = anime["seasons"][season_num].get(ep_num)
        title = anime["title"]
        
        try:
            await call.message.answer_video(
                video=file_id,
                caption=f"🎬 <b>{title}</b> — {season_num}-fasl {ep_num}-qism\n\nBizning kanal: {CHANNEL_URL}",
                parse_mode=ParseMode.HTML
            )
            await call.answer()
        except Exception:
            await call.answer("Video yuborishda xatolik yuz berdi!", show_alert=True)
    else:
        await call.answer("Qism topilmadi!", show_alert=True)


async def main():
    logging.basicConfig(level=logging.INFO)
    print("🤖 Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
