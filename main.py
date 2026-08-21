import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandObject, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ANIME BAZASI ---
ANIME_DATABASE = {
    # 1. Arra-odam (Chainsaw Man) 1-13 qismlar
    "csm_1": {"file_id": "BAACAgIAAxkBAAIBjGqITvek1hU9nboe-1P9lGEGpjxDAAIDHwACXKNZSs8JjwrjcGI_PQQ", "title": "Arra-odam — 1-qism"},
    "csm_2": {"file_id": "BAACAgIAAxkBAAIBjmqIUEYWJKZowMVK27oQpnPFqfFkAAJ_IwACW3VgS7zWNDOLr76IPQQ", "title": "Arra-odam — 2-qism"},
    "csm_3": {"file_id": "BAACAgIAAxkBAAIBkGqIUEpwlOlr5v7gGhoeV3B2iQiNAAIEIgAClYgQSzoDERkp59oHPQQ", "title": "Arra-odam — 3-qism"},
    "csm_4": {"file_id": "BAACAgIAAxkBAAIBkmqIUE6eSoMqzigxkohaJwrIPZMbAAJyIgACqNGgS0hxSlxKQdYVPQQ", "title": "Arra-odam — 4-qism"},
    "csm_5": {"file_id": "BAACAgIAAxkBAAIBlGqIUFKSgnZFOcovupcfJtcZSzPlAAK0IQACPaWBSwqr39AAAbWO5D0E", "title": "Arra-odam — 5-qism"},
    "csm_6": {"file_id": "BAACAgIAAxkBAAIBlmqIUFbDKzWO15pJefRboIJqD3r0AAMeAAJE8flLmyi689aR8jA9BA", "title": "Arra-odam — 6-qism"},
    "csm_7": {"file_id": "BAACAgIAAxkBAAIBmGqIUForW-Aw9tUsowHiD9PtP5DgAAKDIwACPnQgSD-Sn_cMPd0tPQQ", "title": "Arra-odam — 7-qism"},
    "csm_8": {"file_id": "BAACAgIAAxkBAAIBmmqIUF64dJ6QMNbqy63_kwnV8E6dAAIZKQAC3TdASvDSAiWwvPGdPQQ", "title": "Arra-odam — 8-qism"},
    "csm_9": {"file_id": "BAACAgIAAxkBAAIBnGqIUGLsvI59Ix7uiBwHdt-wHcaTAAIsNQAC3BAoSH26CMRr7p1ePQQ", "title": "Arra-odam — 9-qism"},
    "csm_10": {"file_id": "BAACAgIAAxkBAAIBnmqIUGVAX6DnhNfR-IbNV1fQ87pKAAI2NQAC3BAoSFFJQNyPhiX3PQQ", "title": "Arra-odam — 10-qism"},
    "csm_11": {"file_id": "BAACAgIAAxkBAAIBoGqIUGqdBdMOs1p6dJffxX9Q9ANEAAJENQAC3BAoSOauMhlNiQxRPQQ", "title": "Arra-odam — 11-qism"},
    "csm_12": {"file_id": "BAACAgIAAxkBAAIBomqIUG6ROElwqajBRkvFlQABHF9SjgACVjUAAtwQKEjJ05nmrrPThj0E", "title": "Arra-odam — 12-qism"},
    "csm_13": {"file_id": "BAACAgIAAxkBAAIBpGqIUHQNrfIlhDDkVxGnf7biBop2AAIlkgAC80rRSegEI-Ds64PMPQQ", "title": "Arra-odam — 13-qism"},

    # 2. Zombi 100: O'lim oldi ro'yxat (1-12 qismlar) - kodi oddiy raqamlar (1, 2, 3...)
    "1": {"file_id": "BAACAgIAAxkBAAP3aOMrWN2YYARcEa-4NDygo9zwOLYAAjgyAAJGZyBKOYvpww2Wqu89BA", "title": "Zombi 100: O'lim oldi ro'yxat — 1-qism"},
    "2": {"file_id": "BAACAgIAAxkBAAPAaoMrWNWYYARcEa-4NDygo9zwOLYAAjgyAAJGZyBKOYvpww2Wqu89BA", "title": "Zombi 100: O'lim oldi ro'yxat — 2-qism"},
    "3": {"file_id": "BAACAgIAAxkBAAPBaoMrWKpeL_TdQ8fPnOSfDkjjWRAAAoItAAJOqFhKPF6o7oaFIiA9BA", "title": "Zombi 100: O'lim oldi ro'yxat — 3-qism"},
    "4": {"file_id": "BAACAgIAAxkBAAPCaoMrWPDNS-fJhh3ZCDZOEwz74UAAts7AALTfeBKDD-6jImythi9BA", "title": "Zombi 100: O'lim oldi ro'yxat — 4-qism"},
    "5": {"file_id": "BAACAgIAAxkBAAPDaoMrWDIAAVyCgVp5IzlKqczn7UJAAL_MwACmTM4S2AoXyPKNBDrPQQ", "title": "Zombi 100: O'lim oldi ro'yxat — 5-qism"},
    "6": {"file_id": "BAACAgIAAxkBAAPEaoMrWC494xPJnj4mFunfszXBOOMAAp43AAKeybhLOJn6sYqZE0Q9BA", "title": "Zombi 100: O'lim oldi ro'yxat — 6-qism"},
    "7": {"file_id": "BAACAgIAAxkBAAPFaoMrWDZcQ7xry1M-FCsDfRkK5gUAAqs0AALxLnIIQA1xqWBJPG09BA", "title": "Zombi 100: O'lim oldi ro'yxat — 7-qism"},
    "8": {"file_id": "BAACAgIAAxkBAAPGaoMrWDPq0re9FfptyQRwOqHUX1AAArE0AALxLnII3fXjzO3flk49BA", "title": "Zombi 100: O'lim oldi ro'yxat — 8-qism"},
    "9": {"file_id": "BAACAgIAAxkBAAPHaoMrWCV3ZCJbkMZjPCC6srOHFhcAAvU9AAK8n5FIjtgGPUpNbuA9BA", "title": "Zombi 100: O'lim oldi ro'yxat — 9-qism"},
    "10": {"file_id": "BAACAgIAAxkBAAPIaoMrWDg6OUZF1SRmu13HNIAOjf4AAq9CAAJ9wlFIL_Vc04HNKi09BA", "title": "Zombi 100: O'lim oldi ro'yxat — 10-qism"},
    "11": {"file_id": "BAACAgIAAxkBAAPJaoMrWKqmMuZLE02W7t5IICz6psMAAp5AAAJ-1WhImMLnoZob7cM9BA", "title": "Zombi 100: O'lim oldi ro'yxat — 11-qism"},
    "12": {"file_id": "BAACAgIAAxkBAAPKaoMrWObCk_yw-wn2gB0AATmJ-vGnAAJyNwACmmKASIvYF4yXj8b9PQQ", "title": "Zombi 100: O'lim oldi ro'yxat — 12-qism"},

    # 3. Akademiyaning birinchi raqamli boy qiziga yashirincha enagalik qiladigan bo'ldim (1-6 qismlar)
    "boyqiz_1": {"file_id": "BAACAgIAAxkBAAIBvmQ6uCIBQx6ZzcPotiUSZN-LPxCAAIapgAC51hoSjssBuD_2phrPQQ", "title": "Enagalik qiladigan bo'ldim — 1-qism"},
    "boyqiz_2": {"file_id": "BAACAgIAAxkBAAIBv2qG6vI62sHwPoaZWI30u-65AAFNoAACapsAAJiToEoaVkHC4Zv7ED0E", "title": "Enagalik qiladigan bo'ldim — 2-qism"},
    "boyqiz_3": {"file_id": "BAACAgIAAxkBAAIBwGqG6vZ3dtf7S9YdFLKmpjop49DAAIErWAC38noSp0cgRXrYW1LPQQ", "title": "Enagalik qiladigan bo'ldim — 3-qism"},
    "boyqiz_4": {"file_id": "BAACAgIAAxkBAAIBwmqG6vuVr1X0Ygr3Wt2TmcXZAAEA0QACBKgAAhhdQUuGwUSkzlvu0z0E", "title": "Enagalik qiladigan bo'ldim — 4-qism"},
    "boyqiz_5": {"file_id": "BAACAgIAAxkBAAIBxGqG6wS0q_hvZuPVA3c3oX2FjyE7AALoqqAC3C2AS5COMOI9-bHyPQQ", "title": "Enagalik qiladigan bo'ldim — 5-qism"},
    "boyqiz_6": {"file_id": "BAACAgQAAxkBAAIBW2qG6wtI90-ZDH0YTWD3TW0iTo3_AAJZhgACF6LoUz3imBALBhDOPQQ", "title": "Enagalik qiladigan bo'ldim — 6-qism"}
}

# --- TUGMA MENYULARI ---
def get_chainsaw_menu():
    buttons = []
    row = []
    for ep in range(1, 14):
        row.append(InlineKeyboardButton(text=f"{ep}-qism", callback_data=f"send_csm_{ep}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_zom100_menu():
    buttons = []
    row = []
    for ep in range(1, 13):
        row.append(InlineKeyboardButton(text=f"{ep}-qism", callback_data=f"send_zom_{ep}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_boyqiz_menu():
    buttons = []
    row = []
    for ep in range(1, 7):
        row.append(InlineKeyboardButton(text=f"{ep}-qism", callback_data=f"send_bq_{ep}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🪚 Arra-odam (Chainsaw Man)", callback_data="show_csm")],
            [InlineKeyboardButton(text="🧟 Zombi 100", callback_data="show_zom")],
            [InlineKeyboardButton(text="👧 Akademiyaning birinchi raqamli boy qizi...", callback_data="show_bq")],
            [InlineKeyboardButton(text="📺 Anime kodi orqali qidirish", callback_data="search_code")],
            [InlineKeyboardButton(text="🔍 Anime nomi orqali qidirish", callback_data="search_name")],
            [InlineKeyboardButton(text="🎭 Janr tanlash", callback_data="select_genre")],
            [InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/aniwertyn1")]
        ]
    )

# --- DEEP LINKING VA START HANDLER ---
@dp.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    args = command.args

    if args and args in ANIME_DATABASE:
        anime_data = ANIME_DATABASE[args]
        await message.answer_video(
            video=anime_data["file_id"],
            caption=(
                f"🎬 **{anime_data.get('title', 'Anime')}**\n\n"
                f"🔢 **Anime kodi:** `{args}`\n"
                f"📢 **Kanalimiz:** @aniwertyn1"
            )
        )
        return

    await message.answer("Kerakli bo'limni tanlang yoki anime kodini yuboring 👇", reply_markup=get_main_keyboard())

# --- CALLBACK HANDLERS ---
@dp.callback_query(F.data == "show_csm")
async def process_show_csm(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎬 **Arra-odam (Chainsaw Man)** — Barcha qismlar:\nKerakli qismni tanlang 👇",
        reply_markup=get_chainsaw_menu()
    )
    await callback.answer()

@dp.callback_query(F.data == "show_zom")
async def process_show_zom(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎬 **Zombi 100: O'lim oldi ro'yxat** — Barcha qismlar:\nKerakli qismni tanlang 👇",
        reply_markup=get_zom100_menu()
    )
    await callback.answer()

@dp.callback_query(F.data == "show_bq")
async def process_show_bq(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎬 **Akademiyaning birinchi raqamli boy qiziga yashirincha enagalik qiladigan bo'ldim** — Barcha qismlar:\nKerakli qismni tanlang 👇",
        reply_markup=get_boyqiz_menu()
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("send_csm_"))
async def process_send_csm(callback: types.CallbackQuery):
    ep_num = callback.data.split("_")[2]
    key = f"csm_{ep_num}"
    if key in ANIME_DATABASE:
        anime_data = ANIME_DATABASE[key]
        await callback.message.answer_video(video=anime_data["file_id"], caption=f"🎬 **{anime_data['title']}**\n📢 @aniwertyn1")
        await callback.answer(f"{ep_num}-qism yuborildi!")

@dp.callback_query(F.data.startswith("send_zom_"))
async def process_send_zom(callback: types.CallbackQuery):
    ep_num = callback.data.split("_")[2]
    if ep_num in ANIME_DATABASE:
        anime_data = ANIME_DATABASE[ep_num]
        await callback.message.answer_video(video=anime_data["file_id"], caption=f"🎬 **{anime_data['title']}**\n📢 @aniwertyn1")
        await callback.answer(f"{ep_num}-qism yuborildi!")

@dp.callback_query(F.data.startswith("send_bq_"))
async def process_send_bq(callback: types.CallbackQuery):
    ep_num = callback.data.split("_")[2]
    key = f"boyqiz_{ep_num}"
    if key in ANIME_DATABASE:
        anime_data = ANIME_DATABASE[key]
        await callback.message.answer_video(video=anime_data["file_id"], caption=f"🎬 **{anime_data['title']}**\n📢 @aniwertyn1")
        await callback.answer(f"{ep_num}-qism yuborildi!")

@dp.callback_query(F.data == "back_main")
async def process_back_main(callback: types.CallbackQuery):
    await callback.message.edit_text("Kerakli bo'limni tanlang yoki anime kodini yuboring 👇", reply_markup=get_main_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "search_code")
async def process_code(callback: types.CallbackQuery):
    await callback.message.answer("Anime kodini yuboring (Masalan: 1, csm_1, boyqiz_1...):")
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
            "title": f"Anime kodi: {anime_code}"
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
            caption=f"🎬 **{anime_data.get('title', 'Anime')}**\n🔢 Anime kodi: `{user_code}`\n📢 @aniwertyn1"
        )
    else:
        await message.answer("❌ Bu kod bo'yicha anime topilmadi. Kodni tekshirib qayta yuboring.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
