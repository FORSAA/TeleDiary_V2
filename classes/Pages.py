from libs.PagesLibs import *

class BasePage():
    def __init__(self, tab:Page, user_data:dict):
        self.tab: Page = tab
        self.user_data: dict[str:str] = user_data
        self.url = None
        self.start_date = datetime.strptime("02.09.2024", "%d.%m.%Y")

    LOGOUT_BUTTON = 'a[ng-click="$ctrl.logout()"]'
    SEC_LOGOUT_BUTTON = 'button[ng-click="ctrl.yes()"]'

    async def screenshot(self, to_path:Path, file_name:str='screenshot.png') -> None:
        if not await FilesManager.check_existance(to_path):
            await FilesManager.make_dirs(to_path)

        await self.tab.screenshot(
            path=str(Path(to_path) / file_name)
        )

    async def log_out(self):
        try:
            await self.tab.waitForFunction(f'''() => {{
                const logoutLink = document.querySelector('{BasePage.LOGOUT_BUTTON}');
                return logoutLink && angular.element(logoutLink).scope();
            }}''', timeout=5000)

            await self.tab.evaluate(f'''() => {{
                const logoutLink = document.querySelector('{BasePage.LOGOUT_BUTTON}');
                const scope = angular.element(logoutLink).scope();
                if (scope && scope.$ctrl && scope.$ctrl.logout) {{
                    scope.$ctrl.logout();
                }}
            }}''')

            await self.tab.waitForFunction(f'''() => {{
                const confirmButton = document.querySelector('{BasePage.SEC_LOGOUT_BUTTON}');
                return confirmButton && angular.element(confirmButton).scope();
            }}''', timeout=5000)

            await self.tab.evaluate(f'''() => {{
                const confirmButton = document.querySelector('{BasePage.SEC_LOGOUT_BUTTON}');
                const scope = angular.element(confirmButton).scope();
                if (scope && scope.ctrl && scope.ctrl.yes) {{
                    scope.ctrl.yes();
                }}
            }}''')
        except TimeoutError:
            pass

    async def navigate(self, url:str) -> None:
        await self.tab.goto(url, {'waitUnitl':'load'})
    
    async def click(self, selector:str) -> None:
        await self.tab.waitForSelector(selector, {"visible":True, "timeout":5000})
        await self.tab.click(selector)
    
    async def type_text(self, selector:str, text:str) -> None:
        await self.tab.waitForSelector(selector, {"visible":True, "timeout":5000})
        await self.tab.type(selector, text)
    
    async def wait_for_element(self, selector:str, timeout:int=5000, visibility:bool=True) -> None:
        await self.tab.waitForSelector(selector, {"visible":visibility, "timeout":timeout})

    async def querySelector(self, selector:str):
        await self.tab.waitForSelector(selector, {"visible":True, "timeout":5000})
        return await self.tab.querySelector(selector)
    
    async def querySelectorAll(self, selector:str):
        await self.tab.waitForSelector(selector, {"visible":True, "timeout":5000})
        return await self.tab.querySelectorAll(selector)

class StudentiaryPage(BasePage):
    async def get_data(self) -> dict:
        await self.wait_for_element('select.week_select')
        date = await convert_to_full_date(self.user_data['date'])
        object_id = await get_object_id_from_date(date)
        cur_object_id = await self.tab.querySelectorEval(
            "select.week_select",
            'el => el.value'
        )
        print(f"Date: {self.user_data['date']}\nConverted date: {date}\nCurrent object_id: {cur_object_id}\nFound object_id: {object_id}\n")
        if not object_id==cur_object_id:
            await self.tab.select("select.week_select", object_id)


        response = {
            'success':True,
            'error':{
                'type':'TimeoutError',
                'message':'Запрос выполнен успешно!'
            },
            'data':{
                'schedule':{
                    'type':None,
                    'content': None,
                    'files':None
                }
            }
        }
        return response

class HomePage(BasePage):

    #Selectors
    GO_TO_STUDENTIARY_BUTTON = 'a[ng-click="$ctrl.selectTab(tabItem)"]'

    def __init__(self, tab, user_data):
        super().__init__(tab, user_data)
        self.url = ""
    
    async def go_to_studentiary(self) -> StudentiaryPage:
        await self.tab.waitForFunction(f'''() => {{
            const buttons = document.querySelectorAll('{HomePage.GO_TO_STUDENTIARY_BUTTON}');
            const target = buttons[6];
            return target && angular.element(target).scope();
        }}''', timeout=5000)

        await self.tab.evaluate(f'''() => {{
            const button = document.querySelectorAll('{HomePage.GO_TO_STUDENTIARY_BUTTON}')[6].click();
        }}''')
        return StudentiaryPage(self.tab, self.user_data)

class LoginPage(BasePage):

    # Selectors
    SCHOOLS_SELECTOR = 'li.select2-results__option'
    SCHOOL_NAME_SPAN = "span.select2-selection__rendered"
    SCHOOL_NAME_INPUT = "input.select2-search__field"
    LOGIN_INPUT = "input[name=loginname]"
    PASSWORD_INPUT = "input[name=password]"
    LOGIN_BUTTON = "div.primary-button"
    SECURITY_SKIP_BUTTON = "button.btn-primary"

    def __init__(self, tab:Page, user_data:dict):
        super().__init__(tab, user_data)
        self.url = "https://e-school.obr.lenreg.ru/authorize/login"


    async def security_check(self):
        try:
            await self.tab.waitForFunction(f'''() => {{
                const button = document.querySelector('{LoginPage.SECURITY_SKIP_BUTTON}');
                if (!button) return false;
                const scope = angular.element(button).scope();
                return scope && scope.button;
            }}''', timeout=1500)

            await self.tab.evaluate(f'''() => {{
            const button = document.querySelector('{LoginPage.SECURITY_SKIP_BUTTON}');
            const scope = angular.element(button).scope();
            scope.button.action();
            }}''')
        except TimeoutError:
            pass


    async def login(self) -> HomePage:
        await self.navigate(self.url)

        await self.type_text(LoginPage.LOGIN_INPUT, self.user_data["auth_data"]["login"])
        await self.type_text(LoginPage.PASSWORD_INPUT, self.user_data["auth_data"]["password"])

        try:
            await asyncio.gather(
                self.tab.evaluate(f'''() => {{
                    const div = document.querySelector('{LoginPage.LOGIN_BUTTON}');
                    const scope = angular.element(div).scope();
                    scope.$ctrl.login();
                }}'''),
                self.tab.waitForNavigation({'waitUnitl':'DOMContentLoaded','timeout':3000})
            )
        except TimeoutError:
            response = {
                'success':False,
                'error':{
                    'type':'TimeoutError',
                    'message':'Ошибка авторизации - Неверный логин/пароль или отказано в доступе на сайт по другой, неизвестной причине.\n'
                },
                'data':{
                    'schedule':{
                        'type':None,
                        'content': None,
                        'files':None
                    }
                }
            }
            return response

        await self.security_check()
        return HomePage(self.tab, self.user_data)