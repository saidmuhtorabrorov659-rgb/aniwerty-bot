import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandObject, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ANIME BAZASI (HAMMA QISMLARI BILAN) ---
ANIME_DATABASE = {
    # 1. Zombi 100
    "1": {"file_id": "BAACAgIAAxkBAAPAaoMrWNWYYARcEa-4NDygo9zwOLYAAjgyAAJGZyBKOYvpww2Wqu89BA", "title": "Zombi 100 — 1-qism"},
    "1_1": {"file_id": "BAACAgIAAxkBAAPAaoMrWNWYYARcEa-4NDygo9zwOLYAAjgyAAJGZyBKOYvpww2Wqu89BA", "title": "Zombi 100 — 1-qism"},
    "1_2": {"file_id": "BAACAgIAAxkBAAP3aOMrWN2YYARcEa-4NDygo9zwOLYAAjgyAAJGZyBKOYvpww2Wqu89BA", "title": "Zombi 100 — 2-qism"},
    "1_3": {"file_id": "BAACAgIAAxkBAAPBaoMrWKpeL_TdQ8fPnOSfDkjjWRAAAoItAAJOqFhKPF6o7oaFIiA9BA", "title": "Zombi 100 — 3-qism"},
    "1_4": {"file_id": "BAACAgIAAxkBAAPCaoMrWPDNS-fJhh3ZCDZOEwz74UAAts7AALTfeBKDD-6jImythi9BA", "title": "Zombi 100 — 4-qism"},
    "1_5": {"file_id": "BAACAgIAAxkBAAPDaoMrWDIAAVyCgVp5IzlKqczn7UJAAL_MwACmTM4S2AoXyPKNBDrPQQ", "title": "Zombi 100 — 5-qism"},
    "1_6": {"file_id": "BAACAgIAAxkBAAPEaoMrWC494xPJnj4mFunfszXBOOMAAp43AAKeybhLOJn6sYqZE0Q9BA", "title": "Zombi 100 — 6-qism"},
    "1_7": {"file_id": "BAACAgIAAxkBAAPFaoMrWDZcQ7xry1M-FCsDfRkK5gUAAqs0AALxLnIIQA1xqWBJPG09BA", "title": "Zombi 100 — 7-qism"},
    "1_8": {"file_id": "BAACAgIAAxkBAAPGaoMrWDPq0re9FfptyQRwOqHUX1AAArE0AALxLnII3fXjzO3flk49BA", "title": "Zombi 100 — 8-qism"},
    "1_9": {"file_id": "BAACAgIAAxkBAAPHaoMrWCV3ZCJbkMZjPCC6srOHFhcAAvU9AAK8n5FIjtgGPUpNbuA9BA", "title": "Zombi 100 — 9-qism"},
    "1_10": {"file_id": "BAACAgIAAxkBAAPIaoMrWDg6OUZF1SRmu13HNIAOjf4AAq9CAAJ9wlFIL_Vc04HNKi09BA", "title": "Zombi 100 — 10-qism"},
    "1_11": {"file_id": "BAACAgIAAxkBAAPJaoMrWKqmMuZLE02W7t5IICz6psMAAp5AAAJ-1WhImMLnoZob7cM9BA", "title": "Zombi 100 — 11-qism"},
    "1_12": {"file_id": "BAACAgIAAxkBAAPKaoMrWObCk_yw-wn2gB0AATmJ-vGnAAJyNwACmmKASIvYF4yXj8b9PQQ", "title": "Zombi 100 — 12-qism"},

    # 2. Akademiyaning birinchi raqamli boy qiziga...
    "2": {"file_id": "BAACAgIAAxkBAAIBvmQ6uCIBQx6ZzcPotiUSZN-LPxCAAIapgAC51hoSjssBuD_2phrPQQ", "title": "Enagalik qiladigan bo'ldim — 1-qism"},
    "2_1": {"file_id": "BAACAgIAAxkBAAIBvmQ6uCIBQx6ZzcPotiUSZN-LPxCAAIapgAC51hoSjssBuD_2phrPQQ", "title": "Enagalik qiladigan bo'ldim — 1-qism"},
    "2_2": {"file_id": "BAACAgIAAxkBAAIBv2qG6vI62sHwPoaZWI30u-65AAFNoAACapsAAJiToEoaVkHC4Zv7ED0E", "title": "Enagalik qiladigan bo'ldim — 2-qism"},
    "2_3": {"file_id": "BAACAgIAAxkBAAIBwGqG6vZ3dtf7S9YdFLKmpjop49DAAIErWAC38noSp0cgRXrYW1LPQQ", "title": "Enagalik qiladigan bo'ldim — 3-qism"},
    "2_4": {"file_id": "BAACAgIAAxkBAAIBwmqG6vuVr1X0Ygr3Wt2TmcXZAAEA0QACBKgAAhhdQUuGwUSkzlvu0z0E", "title": "Enagalik qiladigan bo'ldim — 4-qism"},
    "2_5": {"file_id": "BAACAgIAAxkBAAIBxGqG6wS0q_hvZuPVA3c3oX2FjyE7AALoqqAC3C2AS5COMOI9-bHyPQQ", "title": "Enagalik qiladigan bo'ldim — 5-qism"},
    "2_6": {"file_id": "BAACAgQAAxkBAAIBW2qG6wtI90-ZDH0YTWD3TW0iTo3_AAJZhgACF6LoUz3imBALBhDOPQQ", "title": "Enagalik qiladigan bo'ldim — 6-qism"},

    # 3. Arra-odam (Chainsaw Man)
    "3": {"file_id": "BAACAgIAAxkBAAIBjGqITvek1hU9nboe-1P9lGEGpjxDAAIDHwACXKNZSs8JjwrjcGI_PQQ", "title": "Arra-odam — 1-qism"},
    "3_1": {"file_id": "BAACAgIAAxkBAAIBjGqITvek1hU9nboe-1P9lGEGpjxDAAIDHwACXKNZSs8JjwrjcGI_PQQ", "title": "Arra-odam — 1-qism"},
    "3_2": {"file_id": "BAACAgIAAxkBAAIBjmqIUEYWJKZowMVK27oQpnPFqfFkAAJ_IwACW3VgS7zWNDOLr76IPQQ", "title": "Arra-odam — 2-qism"},
    "3_3": {"file_id": "BAACAgIAAxkBAAIBkGqIUEpwlOlr5v7gGhoeV3B2iQiNAAIEIgAClYgQSzoDERkp59oHPQQ", "title": "Arra-odam — 3-qism"},
    "3_4": {"file_id": "BAACAgIAAxkBAAIBkmqIUE6eSoMqzigxkohaJwrIPZMbAAJyIgACqNGgS0hxSlxKQdYVPQQ", "title": "Arra-odam — 4-qism"},
    "3_5": {"file_id": "BAACAgIAAxkBAAIBlGqIUFKSgnZFOcovupcfJtcZSzPlAAK0IQACPaWBSwqr39AAAbWO5D0E", "title": "Arra-odam — 5-qism"},
    "3_6": {"file_id": "BAACAgIAAxkBAAIBlmqIUFbDKzWO15pJefRboIJqD3r0AAMeAAJE8flLmyi689aR8jA9BA", "title": "Arra-odam — 6-qism"},
    "3_7": {"file_id": "BAACAgIAAxkBAAIBmGqIUForW-Aw9tUsowHiD9PtP5DgAAKDIwACPnQgSD-Sn_cMPd0tPQQ", "title": "Arra-odam — 7-qism"},
    "3_8": {"file_id": "BAACAgIAAxkBAAIBmmqIUF64dJ6QMNbqy63_kwnV8E6dAAIZKQAC3TdASvDSAiWwvPGdPQQ", "title": "Arra-odam — 8-qism"},
    "3_9": {"file_id": "BAACAgIAAxkBAAIBnGqIUGLsvI59Ix7uiBwHdt-wHcaTAAIsNQAC3BAoSH26CMRr7p1ePQQ", "title": "Arra-odam — 9-qism"},
    "3_10": {"file_id": "BAACAgIAAxkBAAIBnmqIUGVAX6DnhNfR-IbNV1fQ87pKAAI2NQAC3BAoSFFJQNyPhiX3PQQ", "title": "Arra-odam — 10-qism"},
    "3_11": {"file_id": "BAACAgIAAxkBAAIBoGqIUGqdBdMOs1p6dJffxX9Q9ANEAAJENQAC3BAoSOauMhlNiQxRPQQ", "title": "Arra-odam — 11-qism"},
    "3_12": {"file_id": "BAACAgIAAxkBAAIBomqIUG6ROElwqajBRkvFlQABHF9SjgACVjUAAtwQKEjJ05nmrrPThj0E", "title": "Arra-odam — 12-qism"},
    "3_13": {"file_id": "BAACAgIAAxkBAAIBpGqIUHQNrfIlhDDkVxGnf7biBop2AAIlkgAC80rRSegEI-Ds64PMPQQ", "title": "Arra-odam — 13-qism"}
}

# --- MENYULAR ---
def get_chainsaw_menu():
    buttons = []
    row = []
    for ep in range(1, 14):
        row.append(InlineKeyboardButton(text=f"{ep}-qism", callback_data=f"send_3_{ep}"))
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
        row.append(InlineKeyboardButton(text=f"{ep}-qism", callback_data=f"send_1_{ep}"))
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
        row.append(InlineKeyboardButton(text=f"{ep}-qism", callback_data=f"send_2_{ep}"))
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
            [InlineKeyboardButton(text="🧟 Zombi 100 (Kodi: 1)", callback_data="show_zom")],
            [InlineKeyboardButton(text="👧 Boy qizga enagalik... (Kodi: 2)", callback_data="show_bq")],
            [InlineKeyboardButton(text="🪚 Arra-odam (Kodi: 3)", callback_data="show_csm")],
            [InlineKeyboardButton(text="📺 Anime kodi orqali qidirish", callback_data="search_code")],
            [InlineKeyboardButton(text="🔍 Anime nomi orqali qidirish", callback_data="search_name")],
            [InlineKeyboardButton(text="🎭 Janr tanlash", callback_data="select_genre")],
            [InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/aniwertyn1")]
        ]
    )

# --- START HANDLER ---
@dp.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    args = command.args

    if args:
        if args == "1":
            await message.answer("🎬 **Zombi 100: O'lim oldi ro'yxat** — Qismlar:", reply_markup=get_zom100_menu())
            return
        elif args == "2":
            await message.answer("🎬 **Akademiyaning birinchi raqamli boy qizi...** — Qismlar:", reply_markup=get_boyqiz_menu())
            return
        elif args == "3":
            await message.answer("🎬 **Arra-odam (Chainsaw Man)** — Qismlar:", reply_markup=get_chainsaw_menu())
            return
        elif args in ANIME_DATABASE:
            anime_data = ANIME_DATABASE[args]
            await message.answer_video(video=anime_data["file_id"], caption=f"🎬 **{anime_data['title']}**\n📢 @aniwertyn1")
            return

    await message.answer("Kerakli bo'limni tanlang yoki anime kodini yuboring 👇", reply_markup=get_main_keyboard())

# --- CALLBACK HANDLERS ---
@dp.callback_query(F.data == "show_csm")
async def process_show_csm(callback: types.CallbackQuery):
    await callback.message.edit_text("🎬 **Arra-odam (Chainsaw Man)** — Qismlar:", reply_markup=get_chainsaw_menu())
    await callback.answer()

@dp.callback_query(F.data == "show_zom")
async def process_show_zom(callback: types.CallbackQuery):
    await callback.message.edit_text("🎬 **Zombi 100** — Qismlar:", reply_markup=get_zom100_menu())
    await callback.answer()

@dp.callback_query(F.data == "show_bq")
async def process_show_bq(callback: types.CallbackQuery):
    await callback.message.edit_text("🎬 **Boy qizga enagalik...** — Qismlar:", reply_markup=get_boyqiz_menu())
    await callback.answer()

@dp.callback_query(F.data.startswith("send_"))
async def process_send_ep(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    key = f"{parts[1]}_{parts[2]}"
    if key in ANIME_DATABASE:
        anime_data = ANIME_DATABASE[key]
        await callback.message.answer_video(video=anime_data["file_id"], caption=f"🎬 **{anime_data['title']}**\n📢 @aniwertyn1")
        await callback.answer("Qism yuborildi!")

@dp.callback_query(F.data == "back_main")
async def process_back_main(callback: types.CallbackQuery):
    await callback.message.edit_text("Kerakli bo'limni tanlang yoki anime kodini yuboring 👇", reply_markup=get_main_keyboard())
    await callback.answer()

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

# --- CHATDA KOD YUBORGANDA ---
@dp.message(F.text)
import os
from aiohttp import web

# Render web-service o'chib qolmasligi uchun ping sahifasi
async def handle(request):
    return web.Response(text="Bot faol ishlamoqda!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render avto-taqdim etadigan PORT ni olish
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    # Web serverni orqa fonda yurgizish
    await start_web_server()
    
    # Bot pollingini boshlash
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
