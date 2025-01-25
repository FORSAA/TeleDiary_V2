from libs.browserManagerLibs import *
import time

TEST_AUTH_DATA = ast.literal_eval(os.getenv('TEST_AUTH_DATA'))

TEST_REQUEST_DATA = {
    "auth_data" : TEST_AUTH_DATA,
    'type' : "text",
    'date' : "28 Января"
}

class BrowserManager:

    BROWSER_ARGS: dict = {
        'headless': True,
        'args': [
            '--disable-infobars',
            '--disable-features=DownloadBubble',
            '-disable-animations',
            '--disable-software-rasterizer',
            '--start-fullscreen'
        ], # , '--start-fullscreen'
        'defaultViewport': {
            'width':1920,
            'height':1080,
        }
    }

    @staticmethod
    async def main():
        await FilesManager.clear_dir('temp')

        start_time = time.time()
        browser = await launch(
            BrowserManager.BROWSER_ARGS
        )
        print(f"\n - Browser Initialized")

        tab = await browser.newPage()
        print(f" - - Tab Initialized")

        await tab.setCookie(
            {
                'name':'TTSLogin',
                'value':'SCID=180&PID=0&CID=0&SID=0&SFT=0&CN=0&BSP=0',
                'url':'https://e-school.obr.lenreg.ru/authorize/login'
            }
        )
        print(f" - - Cookie sent")
        prepare_end_time = time.time()

        page = LoginPage(tab, TEST_AUTH_DATA)
        print(f" - - PageClass created\n")

        print(f" - Login process started")
        login_time_start = time.time()
        page: HomePage = await page.login()
        login_time_end = time.time()
        print(f" - - Login process finished\n")

        screenshot_time_start = time.time()
        await page.screenshot(Path('temp')/'user_0'/'pics', 'screen.png')
        screenshot_time_end = time.time()

        print(f" - Logout process started")
        logout_time_start = time.time()
        await page.log_out()
        logout_time_end = time.time()
        print(f" - - Logout process finished\n")

        await browser.close()
        print(f" - Browser closed")
        end_time = time.time()

        print(
            '- - - - TIMINGS - - - -\n'
            f'+ Ready to work time: {round(prepare_end_time-start_time,2)} sec.\n'
            f'+ Login time: {round(login_time_end-login_time_start,2)} sec.\n'
            f'+ Screenshot time: {round(screenshot_time_end-screenshot_time_start,2)} sec.\n'
            f'+ Logout time: {round(logout_time_end-logout_time_start,2)} sec.\n'
            f'+ Closing browser time: {round(end_time-logout_time_end,2)} sec.\n'
            f'= = = Full time: {round(end_time-start_time,2)} sec.\n'

        )