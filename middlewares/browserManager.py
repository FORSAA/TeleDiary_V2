from libs.browserManagerLibs import *
import time

RED,RESET = '\033[91m','\033[0m'

BROWSER_ARGS: dict = {
    'headless': True,
    'args': [
        '--disable-infobars',
        '--disable-features=DownloadBubble',
        '-disable-animations',
        '--disable-software-rasterizer',
        #'--start-fullscreen'
    ],
    'defaultViewport': {
        'width':1920,
        'height':1080,
    }
}


class BrowserManager:

    def __init__(self):
        self.browser = None

    async def launch_browser(self):
        self.browser = await launch(
            BROWSER_ARGS
        )

    async def get_homework(self, request_data:dict):
        tab = await self.browser.newPage()
        await tab.setCookie(
            {
                'name':'TTSLogin',
                'value':'SCID=180&PID=0&CID=0&SID=0&SFT=0&CN=0&BSP=0',
                'url':'https://e-school.obr.lenreg.ru/authorize/login'
            }
        )
        page = LoginPage(tab, request_data)

        result: HomePage|dict = await page.login()

        if isinstance(result, HomePage):
            page: HomePage = result
        else:
            if result['error']['type']:
                await page.tab.close()
                return f"{RED}{result['error']['message']}{RESET}"

        await page.log_out()
        await page.tab.close()
        return "all good"