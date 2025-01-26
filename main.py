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
    await browser_manager.get_homework(TEST_REQUEST_DATA1)

    await asyncio.sleep(5)
    await browser_manager.browser.close()

asyncio.run(main())