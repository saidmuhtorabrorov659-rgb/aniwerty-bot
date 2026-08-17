import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Zombi 100 qismlarining file_id bazasi
ANIME_DATABASE = {
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

# Opisaniya matnini tayyorlaydigan funksiya
def get_anime_caption(ep_num: str) -> str:
    return (
        f"🎬 *Anime:* Zombi 100: O'lim oldi roʻyxat\n"
        f"📌 *Qism:* {ep_num}-qism\n"
        f"🎥 *Qismlar soni:* 12\n"
        f"🇺🇿 *Tili:* O'zbekcha\n"
        f"🎭 *Janri:* Komediya, Ekshn, Sarguzasht\n"
        f"🟢 *Holati:* Tugagan\n\n"
        f"📢 *Kanal:* @aniwertyn1\n\n"
        f"👇 *Boshqa qismlarni tomosha qilish uchun tanlang:*"
    )

def get_episodes_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1-qism", callback_data="ep_1"),
                InlineKeyboardButton(text="2-qism", callback_data="ep_2"),
                InlineKeyboardButton(text="3-qism", callback_data="ep_3"),
                InlineKeyboardButton(text="4-qism", callback_data="ep_4"),
            ],
            [
                InlineKeyboardButton(text="5-qism", callback_data="ep_5"),
                InlineKeyboardButton(text="6-qism", callback_data="ep_6"),
                InlineKeyboardButton(text="7-qism", callback_data="ep_7"),
                InlineKeyboardButton(text="8-qism", callback_data="ep_8"),
            ],
            [
                InlineKeyboardButton(text="9-qism", callback_data="ep_9"),
                InlineKeyboardButton(text="10-qism", callback_data="ep_10"),
                InlineKeyboardButton(text="11-qism", callback_data="ep_11"),
                InlineKeyboardButton(text="12-qism", callback_data="ep_12"),
            ],
            [
                InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/aniwertyn1")
            ]
        ]
    )

# --- START HANDLER ---
@dp.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    args = command.args

    if args:
        code = "1" if args in ["1", "zombi100"] else args
        if code in ANIME_DATABASE:
            await message.answer_video(
                video=ANIME_DATABASE[code],
                caption=get_anime_caption(code),
                reply_markup=get_episodes_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
            return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📺 Anime kodi orqali qidirish", callback_data="search_code")],
            [InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/aniwertyn1")]
        ]
    )
    await message.answer("Xush kelibsiz! Anime qismini ko'rish uchun kodingizni yuboring:", reply_markup=keyboard)

@dp.callback_query(F.data == "search_code")
async def process_code(callback: types.CallbackQuery):
    await callback.message.answer("Anime kodini yuboring (Masalan: 1):")
    await callback.answer()

# --- CHATDA RAKAM YUBORGANDA ---
@dp.message(F.text)
async def handle_text_code(message: types.Message):
    code = message.text.strip()
    
    if code in ANIME_DATABASE:
        await message.answer_video(
            video=ANIME_DATABASE[code],
            caption=get_anime_caption(code),
            reply_markup=get_episodes_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.answer("❌ Bu kod bo'yicha anime qismi topilmadi. Qism raqamini to'g'ri kiriting (1 dan 12 gacha).")

# --- INLINE TUGMALAR BOSILGANDA ---
@dp.callback_query(F.data.startswith("ep_"))
async def send_episode(callback: types.CallbackQuery):
    ep_num = callback.data.split("_")[1]
    
    if ep_num in ANIME_DATABASE:
        await callback.message.answer_video(
            video=ANIME_DATABASE[ep_num],
            caption=get_anime_caption(ep_num),
            reply_markup=get_episodes_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
