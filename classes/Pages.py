from libs.PagesLibs import *

class BasePage():
    def __init__(self, tab:Page, user_data:dict):
        self.tab: Page = tab
        self.user_data: dict[str:str] = user_data
        self.url = None

    async def navigate(self, url:str) -> None:
        await self.tab.goto(url, {'waitUnitl':'networkidle2'})
    
    async def click(self, selector:str) -> None:
        await self.tab.waitForSelector(selector)
        await self.tab.click(selector)
    
    async def type_text(self, selector:str, text:str) -> None:
        await self.tab.waitForSelector(selector)
        await self.tab.type(selector, text)
    
    async def wait_for_element(self, selector:str, timeout:int=500):
        await self.tab.waitForSelector(selector, {"timeout":timeout})


class LoginPage(BasePage):

    # Selectors
    LOGIN_INPUT = "input[loginname]"
    PASSWORD_INPUT = "input[password]"

    def __init__(self, tab:Page, user_data:dict):
        super().__init__(tab, user_data)
        self.url = ""
    
    async def login(self):
        await self.navigate(self.url)
        await self.type_text("", self.user_data["login"])
        await self.type_text("", self.user_data["password"])
        await self.click("")
        await self.tab.waitForNavigation()
        return # TODO: HomePage Class
    