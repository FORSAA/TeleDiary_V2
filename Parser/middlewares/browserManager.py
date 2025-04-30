from Parser.libs.browserManagerLibs import *
from main import bot

DEBUG_MODE = False
DOWNLOAD_PATH = Path.cwd()/"temp"

BROWSER_ARGS: dict = {
    'headless': True,
    'args': [
        '--disable-infobars',
        '--no-sandbox',
        '--disable-popup-blocking',
        '--safebrowsing-disable-download-protection',
        '--disable-features=DownloadBubble,DownloadBubbleV2',
        '-disable-animations',
        '--disable-software-rasterizer',
        '--disable-infobars',
        '--disable-web-security',
        '--disable-extensions',
        '--disable-popup-blocking',
        # '--start-fullscreen'
    ],
    'defaultViewport': {
        'width':1000,
        'height':740,
    }
}


class BrowserManager:
    @staticmethod
    async def get_homework(request_data: dict, user_id: int):
        browser = await launch(BROWSER_ARGS)
        user_path = str(DOWNLOAD_PATH / f"{user_id}")
        
        tab = await browser.newPage()
        await tab.setCookie(
            {
                'name': 'TTSLogin',
                'value': 'SCID=180&PID=0&CID=0&SID=0&SFT=0&CN=0&BSP=0',
                'url': 'https://e-school.obr.lenreg.ru/authorize/login'
            }
        )
        client = await tab.target.createCDPSession()
        await client.send('Page.setDownloadBehavior', {
            'behavior': 'allow',
            'downloadPath': str(Path(user_path) / "files"),
        })

        page = LoginPage(tab, request_data, user_id)
        result: HomePage | dict = await page.login()

        if isinstance(result, HomePage):
            page: HomePage = result
        else:
            await browser.close()
            return result

        if page.url != 'https://e-school.obr.lenreg.ru/app/school/studentdiary/':
            page: StudentiaryPage = await page.go_to_studentiary()
        else:
            page: StudentiaryPage = StudentiaryPage(tab, request_data, user_id)

        bot_last_message = await bot.send_message(user_id, "Подготовка данных . . .")
        data: dict = await page.get_data(user_path)
        await bot_last_message.delete()

        await page.log_out()
        await browser.close()

        return data
