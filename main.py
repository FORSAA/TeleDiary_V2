import asyncio, os, json; os.system("cls")
from middlewares import *

TEST_AUTH_DATA = ast.literal_eval(os.getenv('TEST_AUTH_DATA'))


TEST_REQUEST_DATA1 = {
    "auth_data" : TEST_AUTH_DATA,
    'type' : "screenshot",
    'date' :  "22 января"
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
    response = await BrowserManager.get_homework(TEST_REQUEST_DATA1, 55655565)
    if response['success']:
        print(response['data']['schedule']['content'])
        if response['data']['schedule']['type']=='screenshot':print(set(response['data']['links']))

        if DEBUG_MODE:
            print(json.dumps(response, indent=4, ensure_ascii=False))
            print(response['timings'])
    else:
        print(f"Во время выполнения запроса возникла ошибка '{response['error']['type']}'.\nТекст ошибки: {response['error']['message']}")

    await asyncio.sleep(5)
    await FilesManager.rmtree(Path.cwd()/"temp"/"55655565")

asyncio.run(main())