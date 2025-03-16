from libs.browserManagerLibs import *
import time

RED,RESET = '\033[91m','\033[0m'
DEBUG_MODE = True

BROWSER_ARGS: dict = {
    'headless': False,
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
    @staticmethod
    async def get_homework(request_data: dict):
        start_time = time.time()
        browser = await launch(BROWSER_ARGS)
        ready_time = time.time() - start_time

        tab = await browser.newPage()
        await tab.setCookie(
            {
                'name': 'TTSLogin',
                'value': 'SCID=180&PID=0&CID=0&SID=0&SFT=0&CN=0&BSP=0',
                'url': 'https://e-school.obr.lenreg.ru/authorize/login'
            }
        )
        page = LoginPage(tab, request_data)

        login_start_time = time.time()
        result: HomePage | dict = await page.login()
        login_time = time.time() - login_start_time

        if isinstance(result, HomePage):
            page: HomePage = result
        else:
            await browser.close()
            return f"{RED}{result['error']['message']}{RESET}"

        logout_start_time = time.time()
        await page.log_out()
        logout_time = time.time() - logout_start_time

        close_start_time = time.time()
        await browser.close()
        close_time = time.time() - close_start_time

        full_time = time.time() - start_time

        if DEBUG_MODE:
            timings = (
                "\n\n- - - - TIMINGS - - - -\n"
                f"+ Ready to work time: {ready_time:.2f} sec.\n"
                f"+ Login time: {login_time:.2f} sec.\n"
                f"+ Logout time: {logout_time:.2f} sec.\n"
                f"+ Closing browser time: {close_time:.2f} sec.\n"
                f"= = = Full time: {full_time:.2f} sec.\n"
            )
            return timings
        else:
            return "The algorithm completed its work correctly."