import asyncio, os; os.system("cls")
from middlewares.browserManager import *

TEST_AUTH_DATA = ast.literal_eval(os.getenv('TEST_AUTH_DATA'))

TEST_REQUEST_DATA1 = {
    "auth_data" : TEST_AUTH_DATA,
    'type' : "text",
    'date' : "28 Января"
}
TEST_REQUEST_DATA2 = {
    "auth_data" : {
        "login":"Угабуга25",
        "password":"1425"
    },
    'type' : "text",
    'date' : "28 Января"
}

async def main():
    browser_manager = BrowserManager()
    await browser_manager.launch_browser()
    # print(f'Результат №1: {await browser_manager.get_homework(TEST_REQUEST_DATA1)}')
    # print(f'Результат №2: {await browser_manager.get_homework(TEST_REQUEST_DATA2)}')

    results = await asyncio.gather(
        browser_manager.get_homework(TEST_REQUEST_DATA1),
        browser_manager.get_homework(TEST_REQUEST_DATA2)
    )

    for num, result in enumerate(results, start=1):
        print(f'Request №{num} | result: {result}')

    await asyncio.sleep(1.5)
    await browser_manager.browser.close()

asyncio.run(main())