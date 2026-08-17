import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandObject, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Zombi 100 qismlari file_id bazasi
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

# Qismlar uchun knopkalar yaratuvchi funksiya
def get_episodes_keyboard():
    keyboard = InlineKeyboardMarkup(
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
    return keyboard

# --- START VA DEEP LINKING HANDLER ---
@dp.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    args = command.args

    # Agar kanaldan "Tomosha qilish" (zombi100) deb kelinsa
    if args == "zombi100" or args == "1":
        await message.answer_video(
            video=ANIME_DATABASE["1"],
            caption="🎬 **Zombi 100: O'lim oldi roʻyxat – 1-qism**\n\n👇 Boshqa qismlarni tanlang:",
            reply_markup=get_episodes_keyboard()
        )
        return

    # Oddiy start bosilganda
    await message.answer("Xush kelibsiz! Anime qismini ko'rish uchun anime kodini yuboring yoki havoladan kiring.")

# --- INLINE TUGMALAR BOSILGANDA QISM CHIQARISH ---
@dp.callback_query(F.data.startswith("ep_"))
async def send_episode(callback: types.CallbackQuery):
    ep_num = callback.data.split("_")[1]
    
    if ep_num in ANIME_DATABASE:
        await callback.message.answer_video(
            video=ANIME_DATABASE[ep_num],
            caption=f"🎬 **Zombi 100: O'lim oldi roʻyxat – {ep_num}-qism**\n\n👇 Boshqa qismlarni tanlang:",
            reply_markup=get_episodes_keyboard()
        )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
