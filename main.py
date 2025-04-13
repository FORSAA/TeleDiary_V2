import asyncio, os, json; os.system("cls")
from middlewares.browserManager import *
import json

TEST_AUTH_DATA = ast.literal_eval(os.getenv('TEST_AUTH_DATA'))


TEST_REQUEST_DATA1 = {
    "auth_data" : TEST_AUTH_DATA,
    'type' : "screenshot",
    'date' :  "15 апреля"
}

TEST_REQUEST_DATA2 = {
    "auth_data" : {
        "login":"Угабуга25",
        "password":"1425"
    },
    'type' : "text",
    'date' :  "28 Января"
}


async def main():
    response = await BrowserManager.get_homework(TEST_REQUEST_DATA1, 465456)
    if not isinstance(response, dict): print(f'Результат: {response}')
    else: print(json.dumps(response, indent=4, ensure_ascii=False)); print("\n\n\n", response['data']['schedule']['content']);print("\n\n\n", response['data']['links']) 

    # responses = await asyncio.gather(
    #     BrowserManager.get_homework(TEST_REQUEST_DATA1, 465456),
    #     BrowserManager.get_homework(TEST_REQUEST_DATA2, 1854)
    # )
    # async for num, response in astd.enumerate(responses, start=1):
    #     if not isinstance(response, dict): print(f'Результат #{num}: {response}')
    #     else: print(f"Результат №{num}", json.dumps(response, indent=4, ensure_ascii=False))

asyncio.run(main())