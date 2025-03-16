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
    # print(f'Результат: {await BrowserManager.get_homework(TEST_REQUEST_DATA1)}')

    results = await asyncio.gather(
        BrowserManager.get_homework(TEST_REQUEST_DATA1),
        BrowserManager.get_homework(TEST_REQUEST_DATA2)
    )
    async for num, result in astd.enumerate(results, start=1):
        print(f'Request №{num} | result: {result}')

asyncio.run(main())