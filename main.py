import logging
import sys
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8896707660:AAGZ7CpCTVXhiDJFfcycOT_YRyFvC3wU5RE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# To'liq anime bazasi
ANIME_DATABASE = {
    "1": {
        "title": "Zombi 100",
        "total": 12,
        "genre": "Komediya, Ekshn",
        "episodes": {
            "1": "BAACAgIAAxkDAAO_aoMrWJrqEhmS6FrmDMmdP1UgeWAAAtkuAAIh-oBJoEzm5rYLpyg9BA",
            "2": "BAACAgIAAxkDAAPAaoMrWNwYYARcEa-4NDygo9zwOLYAAjgyAAJGZyBKOYvpww2Wqu89BA",
            "3": "BAACAgIAAxkDAAPBaoMrWKpeL_TdQ8fPnOSfDkJjWRAAAoItAAJ0qFhKPF6o7oaFIiA9BA",
            "4": "BAACAgIAAxkDAAPCaoMrWPDNS-fiJhh3ZCDZOEWz74UAAts7AALTfeBKDD-6jImythI9BA",
            "5": "BAACAgIAAxkDAAPDaoMrWDIAAVyYCgVp5IzlKqczn7UJAAL_MwACmTM4S2AoXyPKNBDrPQQ",
            "6": "BAACAgIAAxkDAAPEaoMrWC494xPJnJ4mFunfszXBOOMAAp43AAKeybhLOjn6sYqZE0Q9BA",
            "7": "BAACAgIAAxkDAAPFaoMrWDZcQ7xry1M-FCsDfRkK5gUAAqs0AALxLnlIQA1xqWBJPG09BA",
            "8": "BAACAgIAAxkDAAPGaoMrWDPq0re9FfptyQRwOqHUx1AAArE0AALxLnlI3fXJzO3flk49BA",
            "9": "BAACAgIAAxkDAAPHaoMrWCV3ZCJbkMZjPCC6srOHFhcAAvU9AAK8n5FIjtqGPUpNbuA9BA",
            "10": "BAACAgIAAxkDAAPIaoMrWDg6OUZF1SRmu13HNIAOjf4AAq9CAAJ9wlFIL_Vc04HNKi09BA",
            "11": "BAACAgIAAxkDAAPJaoMrWKqmMuZLE02W7t5IlCz6psMAAp5AAAJ-1WhImMLnoZob7cM9BA",
            "12": "BAACAgIAAxkDAAPKaoMrWObCk_yw-wn2gB0AATmJ-vGnAAJyNwACmmKASIvYF4yXj8b9PQQ"
        }
    },
    "2": {
        "title": "Akademiyaning birinchi raqamli boy qiziga yashirincha enagalik qiladigan boʻldim",
        "total": 12,
        "genre": "Romantika",
        "episodes": {
            "1": "BAACAgIAAxkDAAIBVmqG6uCIBQx6ZzcPotiUSZN-lPxCAAIapgAC51hoSjssBuD_2phrPQQ",
            "2": "BAACAgIAAxkDAAIBV2qG6vI62sHwPoaZWI30u-65AAFNoAACapsAAjItoEoaVkHC4Zv7ED0E",
            "3": "BAACAgIAAxkDAAIBWGqG6vZ3dtf7S9YdFLKmpjop49mDAAIErwAC38noSp0cgRXrYWllPQQ",
            "4": "BAACAgIAAxkDAAIBWWqG6vuVr1X0Ygr3Wt2TmcXZAAEa0QACBKgAAhhdQUuGwUSkz1vu0z0E",
            "5": "BAACAgIAAxkDAAIBWmqG6wSOq_hvZuPVA3c3oX2FjyE7AALoqgAC3C2AS5COMOI9-bHyPQQ",
            "6": "BAACAgQAAxkBAAIBW2qG6wtI9O-ZDH0YTWDBTW0iTo3_AAJZHgACF6LoUz3imBALBhDOPQQ"
        }
    },
    "3": {
        "title": "Arra Odam (Chainsaw Man)",
        "total": 13,
        "genre": "Ekshn, Qorong'u Fentezi, Shounen",
        "episodes": {
            "1": "BAACAgIAAxkDAAIB7mqJQdvtq0_8TqJX0MkL7PFL7zsYAAIDHwACXKNZs8JjwrjcGI_PQQ",
            "2": "BAACAgIAAxkDAAIB72qJYXtAaYpxoqtecyI5JwAB7MdPpAgACfYMAA1t1YEu81jQzi6--ID0E",
            "3": "BAACAgIAAxkDAAICWqJnunHnWC6RxmqAWiWyEX33asAAIEIgACLYgQSzoDERkp59oHPQQ",
            "4": "BAACAgIAAxkDAAIC2qJnuzCir_Tqcc603qAQcskk95caAJyIgAcQNGgS0hxS1xKQdYVPQQ",
            "5": "BAACAgIAAxkDAAICWqJnxH6rmNIQfsoB9qR0cN-vmhnAAK0IQACPaWBSwqr39AAAbW05D0E",
            "6": "BAACAgIAAxkDAAICJ2qJnxcmlwXLARgTveGY0410YP2hAaAMEAAJE8flLmyi689aRjA9BA",
            "7": "BAACAgIAAxkDAAICKWqJnxtfJgLeUKV61WTLuAAB_Oxx8wACgyMAAj50IEg_kp_3DD3dLTr0E",
            "8": "BAACAgIAAxkDAAICK2qJnx9mUp34Qbk_z_RuJQyg1m2wAAIZKQAC3DaSvDSAiWvPGdPQQA",
            "9": "BAACAgIAAxkDAAICLWqJnybZ6pEyCdqEerk32_y-WRyPAAiSNQAC3BAoSH26CMRr7plEPQQ",
            "10": "BAACAgIAAxkDAAICL2qJnyo5a94Y0t4JJmBrp86hmIBTAAI2NQAC3BAoSFFJQNyPhI3PQQ",
            "11": "BAACAgIAAxkDAAICMWqJny2ahrLKVfRkEP57reNZuDFIAAJENQAC3BAoS0AuMh1NiQxRPQQ",
            "12": "BAACAgIAAxkDAAICWqJnYQJYUTipI3bcvscSBvCB_zVtnlAAAJWNQAIC3BAoSMnTmeaus90GPQQ",
            "13": "BAACAgIAAxkDAAICNWqJnzcvGn80UUZCG9nm6_pLkxV-AAILkgAC80rRSegEI-Ds64PMPQQ"
        }
    }
}

def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📺 Anime kodi orqali qidirish", callback_data="search_by_code")],
        [InlineKeyboardButton(text="🔍 Anime nomi orqali qidirish", callback_data="search_by_name")],
        [InlineKeyboardButton(text="🎭 Janr tanlash", callback_data="select_genre")],
        [InlineKeyboardButton(text="📢 Asosiy kanal", url="https://t.me/aniwertyn1")]
    ])

def get_episodes_keyboard(anime_key: str):
    anime = ANIME_DATABASE[anime_key]
    buttons = []
    row = []
    for ep_num in range(1, anime["total"] + 1):
        row.append(InlineKeyboardButton(text=str(ep_num), callback_data=f"ep_{anime_key}_{ep_num}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Xush kelibsiz! Kerakli bo'limni tanlang yoki anime kodini yuboring 👇",
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.MARKDOWN
    )

@dp.callback_query(F.data == "search_by_code")
async def search_code_cb(callback: types.CallbackQuery):
    text = "🔢 **Mavjud animelar va kodlari:**\n\n"
    for code, data in ANIME_DATABASE.items():
        text += f"Kodi: `{code}` — {data['title']}\n"
    text += "\nKerakli anime kodini yuboring (masalan: `3`):"
    await callback.message.edit_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")]
    ]))
    await callback.answer()

@dp.callback_query(F.data == "search_by_name")
async def search_name_cb(callback: types.CallbackQuery):
    await callback.message.answer("Anime nomini yozib yuboring 🔍")
    await callback.answer()

@dp.callback_query(F.data == "select_genre")
async def genre_cb(callback: types.CallbackQuery):
    await callback.message.answer("Janrni tanlang 🎭")
    await callback.answer()

@dp.message(F.text)
async def handle_code_input(message: types.Message):
    code = message.text.strip()
    if code in ANIME_DATABASE:
        anime = ANIME_DATABASE[code]
        text = f"🎬 **{anime['title']}**\n\n📌 **Janr:** {anime['genre']}\n🔢 **Qismlar soni:** {anime['total']} ta\n\nQismni tanlang:"
        await message.answer(text, reply_markup=get_episodes_keyboard(code), parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("⚠️ Bunday kodli anime topilmadi!")

@dp.callback_query(F.data.startswith("ep_"))
async def send_episode(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    anime_key = parts[1]
    ep_num = parts[2]  # Endi 10, 11, 12, 13 ham to'g'ri ishlaydi
    
    file_id = ANIME_DATABASE.get(anime_key, {}).get("episodes", {}).get(ep_num)
    
    if file_id:
        await callback.message.answer_video(
            video=file_id,
            caption=f"🎬 {ANIME_DATABASE[anime_key]['title']} — {ep_num}-qism",
            reply_markup=get_episodes_keyboard(anime_key)
        )
    else:
        await callback.answer("⚠️ Bu qism hali qo'shilmagan!", show_alert=True)
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Xush kelibsiz! Kerakli bo'limni tanlang yoki anime kodini yuboring 👇",
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.MARKDOWN
    )
    await callback.answer()

if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
