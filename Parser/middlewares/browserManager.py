from Parser.libs.browserManagerLibs import *
import time

RED,RESET = '\033[91m','\033[0m'
DEBUG_MODE = False
DOWNLOAD_PATH = Path.cwd()/"temp"

BROWSER_ARGS: dict = {
    'headless': False,
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
    async def get_homework(request_data: dict, user_id:int):
        start_time = time.time()
        browser = await launch(BROWSER_ARGS)

        for proc in psutil.process_iter(['pid', 'name']):
            if 'chrome' in proc.info['name'].lower():
                proc.nice(psutil.HIGH_PRIORITY_CLASS)

        user_path = str(DOWNLOAD_PATH/f"{user_id}")
        
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
            'downloadPath':str(Path(user_path)/"files"),
        })
        ready_time = time.time() - start_time
        page = LoginPage(tab, request_data, user_id)

        login_start_time = time.time()
        result: HomePage | dict = await page.login()
        login_time = time.time() - login_start_time

        work_start_time = time.time()
        if isinstance(result, HomePage):
            page: HomePage = result
        else:
            await browser.close()
            return result
        
        if page.url != 'https://e-school.obr.lenreg.ru/app/school/studentdiary/':
            page:StudentiaryPage = await page.go_to_studentiary()
        else:
            page:StudentiaryPage = StudentiaryPage(tab, request_data, user_id)

        data:dict = await page.get_data(user_path)
        work_time = time.time()-work_start_time

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
                f"+ Work time: {work_time:.2f} sec.\n"
                f"+ Logout time: {logout_time:.2f} sec.\n"
                f"+ Closing browser time: {close_time:.2f} sec.\n"
                f"= = = Full time: {full_time:.2f} sec.\n"
            )
            data['timings'] = timings
            return data
        else:
            return data