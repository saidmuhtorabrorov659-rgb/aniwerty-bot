import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandObject, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Anime bazasi (kod -> file_id va Ma'lumot)
ANIME_DATABASE = {}

# --- DEEP LINKING VA START HANDLER ---
@dp.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    args = command.args  # Tugma bosilganda keladigan parametr (masalan: 1)

    # Agar foydalanuvchi postdagi "Tomosha qilish" tugmasidan kelgan bo'lsa
    if args and args in ANIME_DATABASE:
        anime_data = ANIME_DATABASE[args]
        await message.answer_video(
            video=anime_data["file_id"],
            caption=(
                f"🎬 **{anime_data.get('title', 'Zom 100: Zombiga aylanishdan oldin qiladigan 100 ta ishim')}**\n\n"
                f"🔢 **Anime kodi:** `{args}`\n"
                f"📢 **Kanalimiz:** @aniwertyn1"
            )
        )
        return

    # Oddiy /start bosilganda chiqadigan menyu
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📺 Anime kodi orqali qidirish", callback_data="search_code")],
            [InlineKeyboardButton(text="🔍 Anime nomi orqali qidirish", callback_data="search_name")],
            [InlineKeyboardButton(text="🎭 Janr tanlash", callback_data="select_genre")],
            [InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/aniwertyn1")]
        ]
    )
    await message.answer("Kerakli bo'limni tanlang yoki anime kodini yuboring 👇", reply_markup=keyboard)

# --- CALLBACK HANDLERS ---
@dp.callback_query(F.data == "search_code")
async def process_code(callback: types.CallbackQuery):
    await callback.message.answer("Anime kodini yuboring (Masalan: 1, 2, 3...):")
    await callback.answer()

@dp.callback_query(F.data == "search_name")
async def process_name(callback: types.CallbackQuery):
    await callback.message.answer("Anime nomini yozib yuboring:")
    await callback.answer()

@dp.callback_query(F.data == "select_genre")
async def process_genre(callback: types.CallbackQuery):
    await callback.message.answer("🎭 Janrlar ro'yxati tez orada qo'shiladi.")
    await callback.answer()

# --- ADMIN ANIME VIDEO YUBORGANDA SAQLASH ---
@dp.message(F.video | F.document)
async def handle_anime_upload(message: types.Message):
    file_id = message.video.file_id if message.video else message.document.file_id
    anime_code = message.caption.strip() if message.caption else None

    if anime_code:
        ANIME_DATABASE[anime_code] = {
            "file_id": file_id,
            "title": "Zom 100: Bucket List of the Dead"
        }
        await message.reply(
            f"✅ **Anime bazaga saqlandi!**\n\n"
            f"🔑 **Anime kodi:** `{anime_code}`\n"
            f"🆔 **File ID:** `{file_id}`"
        )
    else:
        await message.reply(
            "📹 **Video qabul qilindi!**\n\n"
            "⚠️ *Kodni saqlash uchun videoni qaytadan yuborib, opisaniyasiga (caption) anime kodini raqam qilib yozing (Masalan: 1)*."
        )

# --- USER ODDY CHATDA KOD YUBORGANDA ---
@dp.message(F.text)
async def handle_text_code(message: types.Message):
    user_code = message.text.strip()
    
    if user_code in ANIME_DATABASE:
        anime_data = ANIME_DATABASE[user_code]
        await message.answer_video(
            video=anime_data["file_id"],
            caption=f"🎬 **Zom 100**\n🔢 Anime kodi: `{user_code}`\n📢 @aniwertyn1"
        )
    else:
        await message.answer("❌ Bu kod bo'yicha anime topilmadi. Kodni tekshirib qayta yuboring.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
