from libs.browserManagerLibs import *
from classes.Pages import *

TEST_AUTH_DATA = ast.literal_eval(os.getenv('TEST_AUTH_DATA'))

TEST_REQUEST_DATA = {
    "auth_data" : TEST_AUTH_DATA,
    'type' : "text",
    'date' : "28 Января"
}

#for var_name, var_content in dict(list(globals().items())[-2:]).items():
#    print(var_name, var_content)

class BrowserManager:

    BROWSER_ARGS: dict = {
        'headless': False,
        'args': ['--disable-infobars', '--disable-features=DownloadBubble'], # , '--start-fullscreen'
        'defaultViewport': {
            'width':1920,
            'height':1080,
        }
    }

    @staticmethod
    async def main():
        pass
        browser = await launch(
            BrowserManager.BROWSER_ARGS
        )

        
        page = await browser.newPage()
        
        await page.goto('http://example.com')
        await page.screenshot({'path': 'temp\\pictures\\example.png'})

        await browser.close()