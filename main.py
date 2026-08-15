import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import web
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# -------------------------------------------------------------
# SHU YERGA ESKI main.py FAYLINDAGI BARCHA HANDLERLARNI QO'YING
# (Masalan: @dp.message(Command("start")), button handlerlar va h.k.)
# -------------------------------------------------------------


# Render va Cron-job uchun ping sahifasi
async def handle(request):
    return web.Response(text="Bot ishlamoqda!")

async def main():
    # Web serverni fonda ishga tushirish (Render portini eshitadi)
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

    # Botni ishga tushirish
    print("@AniWerty_bot muammosiz ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
