import asyncio, os, json, logging, locale, signal; os.system("cls")
from Telebot.libs.mainLibs import *
# from Parser.middlewares.filesManager import *

locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')

states:dict[int, User] = {}
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def start() -> None:
    dp.include_router(handlersRouters)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        print("\n\nStopping . . .")
    # finally:
    #     loop.run_until_complete(FilesManager.clear_dir("temp")); logging.info("Temporary files directory cleared.")
    #     loop.close(); logging.info("Loop closed.")
    #     logging.info("Correctly stopped.")
