import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Anime ma'lumotlari va qismlarining file_id bazasi
ANIME_DATABASE = {
    # 1 - Zombi 100
    "1": {
        "title": "Zombi 100: O'lim oldi roʻyxat",
        "total": 12,
        "genre": "Komediya, Ekshn, Sarguzasht",
        "episodes": {
            "1": "BAACAgIAAxkBAAO_aoMrWJrqEhmS6FrmDMmdP1UgeWAAAtkuAAIh-oBJoEzm5rYLpyg9BA",
            "2": "BAACAgIAAxkBAAPAaoMrWNwYYARcEa-4NDygo9zwOLYAAjgyAAJGZyBKOYvpww2Wqu89BA",
            "3": "BAACAgIAAxkBAAPBaoMrWKpeL_TdQ8fPnOSfDkJjWRAAAoItAAJ0qFhKPF6o7oaFIiA9BA",
            "4": "BAACAgIAAxkBAAPCaoMrWPDNS-fiJhh3ZCDZOEWz74UAAts7AALTfeBKDD-6jImythI9BA",
            "5": "BAACAgIAAxkBAAPDaoMrWDIAAVyYCgVp5IzlKqczn7UJAAL_MwACmTM4S2AoXyPKNBDrPQQ",
            "6": "BAACAgIAAxkBAAPEaoMrWC494xPJnJ4mFunfszXBOOMAAp43AAKeybhLOjn6sYqZE0Q9BA",
            "7": "BAACAgIAAxkBAAPFaoMrWDZcQ7xry1M-FCsDfRkK5gUAAqs0AALxLnlIQA1xqWBJPG09BA",
            "8": "BAACAgIAAxkBAAPGaoMrWDPq0re9FfptyQRwOqHUx1AAArE0AALxLnlI3fXJzO3flk49BA",
            "9": "BAACAgIAAxkBAAPHaoMrWCV3ZCJbkMZjPCC6srOHFhcAAvU9AAK8n5FIjtqGPUpNbuA9BA",
            "10": "BAACAgIAAxkBAAPIaoMrWDg6OUZF1SRmu13HNIAOjf4AAq9CAAJ9wlFIL_Vc04HNKi09BA",
            "11": "BAACAgIAAxkBAAPJaoMrWKqmMuZLE02W7t5IlCz6psMAAp5AAAJ-1WhImMLnoZob7cM9BA",
            "12": "BAACAgIAAxkBAAPKaoMrWObCk_yw-wn2gB0AATmJ-vGnAAJyNwACmmKASIvYF4yXj8b9PQQ"
        }
    },
    # 2 - Akademiyaning birinchi raqamli boy qiziga...
    "2": {
        "title": "Akademiyaning birinchi raqamli boy qiziga yashirincha enagalik qiladigan boʻldim",
        "total": 6,
        "genre": "Romantika, Maktab, Komediya",
        "episodes": {
            "1": "BAACAgIAAxkBAAIBVmqG6uCIBQx6ZzcPotiUSZN-lPxCAAIapgAC51hoSjssBuD_2phrPQQ",
            "2": "BAACAgIAAxkBAAIBV2qG6vI62sHwPoaZWI30u-65AAFNoAACapsAAjItoEoaVkHC4Zv7ED0E",
            "3": "BAACAgIAAxkBAAIBWGqG6vZ3dtf7S9YdFLKmpjop49mDAAIErwAC38noSp0cgRXrYWllPQQ",
            "4": "BAACAgIAAxkBAAIBWWqG6vuVr1X0Ygr3Wt2TmcXZAAEa0QACBKgAAhhdQUuGwUSkz1vu0z0E",
            "5": "BAACAgIAAxkBAAIBWmqG6wSOq_hvZuPVA3c3oX2FjyE7AALoqgAC3C2AS5COMOI9-bHyPQQ",
            "6": "BAACAgQAAxkBAAIBW2qG6wtI9O-ZDH0YTWDBTW0iTo3_AAJZHgACF6LoUz3imBALBhDOPQQ"
        }
    },
    # 3 - Arra-odam (Chainsaw Man)
    "3": {
        "title": "Arra-odam (Chainsaw Man)",
        "total": 12,
        "genre": "Ekshn, Shonen, Triller, Mistik",
        "episodes": {
            "1": "BAACAgIAAxkBAAIBjGqITvek1hU9nboe-1P9lGEGpjxDAAIDHwACXKNZSs8JjwrjcGI_PQQ",
            "2": "BAACAgIAAxkBAAIBjmqIUEYWJKZowMVK27oQpnPFqfFkAAJ_IwACW3VgS7zWNDOLr76IPQQ",
            "3": "BAACAgIAAxkBAAIBkGqIUEpwlOlr5v7gGhoeV3B2iQiNAAIEIgAClYgQSzoDERkp59oHPQQ",
            "4": "BAACAgIAAxkBAAIBkmqIUE6eSoMqzigxkohaJwrIPZMbAAJyIgACqNGgS0hxSlxKQdYVPQQ",
            "5": "BAACAgIAAxkBAAIBlGqIUFKSgnZFOcovupcfJtcZSzPlAAK0IQACPaWBSwqr39AAAbWO5D0E",
            "6": "BAACAgIAAxkBAAIBlmqIUFbDKzWO15pJefRboIJqD3r0AAMeAAJE8flLmyi689aR8jA9BA",
            "7": "BAACAgIAAxkBAAIBmGqIUForW-Aw9tUsowHiD9PtP5DgAAKDIwACPnQgSD-Sn_cMPd0tPQQ",
            "8": "BAACAgIAAxkBAAIBmmqIUF64dJ6QMNbqy63_kwnV8E6dAAIZKQAC3TdASvDSAiWwvPGdPQQ",
            "9": "BAACAgIAAxkBAAIBnGqIUGLsvI59Ix7uiBwHdt-wHcaTAAIsNQAC3BAoSH26CMRr7p1ePQQ",
            "10": "BAACAgIAAxkBAAIBnmqIUGVAX6DnhNfR-IbNV1fQ87pKAAI2NQAC3BAoSFFJQNyPhiX3PQQ",
            "11": "BAACAgIAAxkBAAIBoGqIUGqdBdMOs1p6dJffxX9Q9ANEAAJENQAC3BAoSOauMhlNiQxRPQQ",
            "12": "BAACAgIAAxkBAAIBomqIUG6ROElwqajBRkvFlQABHF9SjgACVjUAAtwQKEjJ05nmrrPThj0E"
        }
    }
}

def get_anime_caption(anime_key: str, ep_num: str) -> str:
    data = ANIME_DATABASE[anime_key]
    return (
        f"🎬 *Anime:* {data['title']}\n"
        f"📌 *Qism:* {ep_num}-qism\n"
        f"🎥 *Qismlar soni:* {data['total']}\n"
        f"🇺🇿 *Tili:* O'zbekcha\n"
        f"🎭 *Janri:* {data['genre']}\n\n"
        f"📢 *Kanal:* @aniwertyn1\n\n"
        f"👇 *Boshqa qismlarni tomosha qilish uchun tanlang:*"
    )

def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📺 Anime kodi orqali qidirish", callback_data="search_code")],
            [InlineKeyboardButton(text="🔍 Anime nomi orqali qidirish", callback_data="search_name")],
            [InlineKeyboardButton(text="🎭 Janr tanlash", callback_data="search_genre")],
            [InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/aniwertyn1")]
        ]
    )

def get_episodes_keyboard(anime_key: str):
    data = ANIME_DATABASE[anime_key]
    total = data["total"]
    
    keyboard = []
    row = []
    for i in range(1, total + 1):
        row.append(InlineKeyboardButton(text=f"{i}-qism", callback_data=f"ep_{anime_key}_{i}"))
        if len(row) == 4:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
        
    keyboard.append([InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/aniwertyn1")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- VIDEO YUBORILGANDA FILE_ID NI CHIQARISH ---
@dp.message(F.video)
async def catch_video_file_id(message: types.Message):
    file_id = message.video.file_id
    await message.reply(f"📁 **Video File ID:**\n`{file_id}`", parse_mode=ParseMode.MARKDOWN)

# --- START HANDLER ---
@dp.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    args = command.args

    if args:
        anime_key = None
        if args == "zombi100":
            anime_key = "1"
        elif args in ANIME_DATABASE:
            anime_key = args

        if anime_key:
            await message.answer_video(
                video=ANIME_DATABASE[anime_key]["episodes"]["1"],
                caption=get_anime_caption(anime_key, "1"),
                reply_markup=get_episodes_keyboard(anime_key),
                parse_mode=ParseMode.MARKDOWN
            )
            return

    await message.answer(
        "Xush kelibsiz! Kerakli bo'limni tanlang yoki anime kodini yuboring 👇",
        reply_markup=get_main_keyboard()
    )

# --- MENYU TUGMALARI ---
@dp.callback_query(F.data == "search_code")
async def process_code(callback: types.CallbackQuery):
    await callback.message.answer("Kerakli anime kodini yuboring 🔢")
    await callback.answer()

@dp.callback_query(F.data == "search_name")
async def process_name(callback: types.CallbackQuery):
    await callback.message.answer("Anime nomini yozib yuboring 🔍")
    await callback.answer()

@dp.callback_query(F.data == "search_genre")
async def process_genre(callback: types.CallbackQuery):
    await callback.message.answer("Hozircha janrlar bo'limi to'ldirilmoqda...")
    await callback.answer()

# --- CHATDA RAQAM YOKI MATN YUBORGANDA ---
@dp.message(F.text)
async def handle_text_code(message: types.Message):
    text = message.text.strip().lower()
    
    if text in ANIME_DATABASE:
        await message.answer_video(
            video=ANIME_DATABASE[text]["episodes"]["1"],
            caption=get_anime_caption(text, "1"),
            reply_markup=get_episodes_keyboard(text),
            parse_mode=ParseMode.MARKDOWN
        )
    elif "enaga" in text or "boy qizi" in text or "akademiya" in text:
        await message.answer_video(
            video=ANIME_DATABASE["2"]["episodes"]["1"],
            caption=get_anime_caption("2", "1"),
            reply_markup=get_episodes_keyboard("2"),
            parse_mode=ParseMode.MARKDOWN
        )
    elif "zom" in text or "zombi" in text:
        await message.answer_video(
            video=ANIME_DATABASE["1"]["episodes"]["1"],
            caption=get_anime_caption("1", "1"),
            reply_markup=get_episodes_keyboard("1"),
            parse_mode=ParseMode.MARKDOWN
        )
    elif "arra" in text or "chainsaw" in text or "csm" in text:
        await message.answer_video(
            video=ANIME_DATABASE["3"]["episodes"]["1"],
            caption=get_anime_caption("3", "1"),
            reply_markup=get_episodes_keyboard("3"),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.answer("❌ Bu kod bo'yicha anime topilmadi. Kodni tekshirib qayta yuboring.")

# --- INLINE QISM TUGMALARI BOSILGANDA ---
@dp.callback_query(F.data.startswith("ep_"))
async def send_episode(callback: types.CallbackQuery):
    _, anime_key, ep_num = callback.data.split("_")
    
    if anime_key in ANIME_DATABASE and ep_num in ANIME_DATABASE[anime_key]["episodes"]:
        await callback.message.answer_video(
            video=ANIME_DATABASE[anime_key]["episodes"][ep_num],
            caption=get_anime_caption(anime_key, ep_num),
            reply_markup=get_episodes_keyboard(anime_key),
            parse_mode=ParseMode.MARKDOWN
        )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
