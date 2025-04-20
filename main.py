import asyncio, os, json, logging, locale, ast; os.system("cls")
from Telebot.libs.mainLibs import *
from Parser.middlewares.filesManager import *

# from Parser.middlewares import *

# TEST_AUTH_DATA = ast.literal_eval(os.getenv('TEST_AUTH_DATA'))

# TEST_REQUEST_DATA1 = {
#     "auth_data" : TEST_AUTH_DATA,
#     'type' : "screenshot",
#     'date' :  "22 января"
# }

# TEST_REQUEST_DATA2 = {
#     "auth_data" : {
#         "login":"Угабуга25",
#         "password":"1425"
#     },
#     'type' : "text",
#     'date' :  "28 Января"
# }


# async def main():
#     response = await BrowserManager.get_homework(TEST_REQUEST_DATA1, 55655565)
#     if response['success']:
#         print(response['data']['schedule']['content'])
#         if response['data']['schedule']['type']=='screenshot':print(set(response['data']['links']))

#         if DEBUG_MODE:
#             print(json.dumps(response, indent=4, ensure_ascii=False))
#             print(response['timings'])
#     else:
#         print(f"Во время выполнения запроса возникла ошибка '{response['error']['type']}'.\nТекст ошибки: {response['error']['message']}")

#     await asyncio.sleep(5)
#     await FilesManager.clear_dir("temp")

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
    finally:
        loop.run_until_complete(FilesManager.clear_dir("temp")); logging.info("Temporary files directory cleared.")
        loop.close(); logging.info("Loop closed.")
        logging.info("Correctly stopped.")
