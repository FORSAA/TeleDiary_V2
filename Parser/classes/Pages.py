from Parser.libs.PagesLibs import *

logger = logging.getLogger("requests.pyppeteer")
logger.setLevel(logging.INFO)
# logger.propagate = False

SELECTORS_OPTIONS = {"visible":True, "timeout":15000}

class BasePage():
    def __init__(self, tab:Page, user_data:dict, user_id:int):
        self.tab: Page = tab
        self.user_data: dict[str:str] = user_data
        self.user_id: int = user_id
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
        await self.tab.waitForSelector(selector, SELECTORS_OPTIONS)
        await self.tab.click(selector)
    
    async def type_text(self, selector:str, text:str) -> None:
        await self.tab.waitForSelector(selector, SELECTORS_OPTIONS)
        await self.tab.type(selector, text)
    
    async def wait_for_element(self, selector:str, timeout:int=5000, visibility:bool=True) -> None:
        await self.tab.waitForSelector(selector, {"visible":visibility, "timeout":timeout})

    async def xpath(self, xpath_selector:str) -> list[ElementHandle]:
        await self.tab.waitForXPath(xpath_selector, SELECTORS_OPTIONS)
        return await self.tab.xpath(xpath_selector)

    async def querySelector(self, selector:str) -> ElementHandle:
        await self.tab.waitForSelector(selector, SELECTORS_OPTIONS)
        return await self.tab.querySelector(selector)
    
    async def querySelectorAll(self, selector:str) -> list[ElementHandle]:
        await self.tab.waitForSelector(selector, SELECTORS_OPTIONS)
        return await self.tab.querySelectorAll(selector)
    
    async def get_element_text(self, element:ElementHandle) -> str:
        _ = await self.tab.evaluate("(el) => el ? el.textContent : null", element)
        if _ is None:
            return ""
        else:
            return _.strip().replace("\t", "").replace("\n", "")
    
        
class StudentiaryPage(BasePage):
    def __init__(self, tab, user_data, user_id):
        super().__init__(tab, user_data, user_id)
    
    async def get_data(self, DOWNLOAD_PATH:str) -> dict:
        response = {
            'success':None,
            'error':{
                'type':None,
                'message':None
            },
            'data':{
                'schedule':{
                    'type':None,
                    'content': None,
                    'files':None
                },
                'links':[]
            }
        }

        links, url_pattern = [], re.compile(r'https?://\S+')

        # self.tab.on("console", lambda msg: logger.info(f"{msg.text()}"))

        await asyncio.sleep(0.25)
        await self.wait_for_element('select.week_select')
        date = await convert_to_full_date(self.user_data['date'])
        object_id = await get_object_id_from_date(date)

        cur_object_id = await self.tab.querySelectorEval(
            "select.week_select",
            'el => el.value'
        )

        if not object_id==cur_object_id:
            await self.tab.select("select.week_select", object_id)

        try:
            tbody:ElementHandle = (await self.xpath(f'//span[contains(text(), "{self.user_data['date']}")]/../../..'))[0]
        except (IndexError, TimeoutError) as e:
            response['success'] = False
            response['error']['type'] = type(e).__name__
            response['error']['message'] = 'Не удалось получить данные из таблицы заданий (Ошибка на стороне сервера портала школы).'
            response['data'] = {}
            return response
        
        match = re.findall(url_pattern, await(await tbody.getProperty('textContent')).jsonValue())
        if match:
            links += match
            response['data']['links'] = links[1::2]

        if self.user_data['type']=='screenshot':
            await self.tab.evaluate(
                f'''() => {{
                    table = document.evaluate('//span[contains(text(), "{self.user_data['date']}")]/../../..', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    table.querySelectorAll('label.icon_dots').forEach(el => el.click());
                }}
                '''
            )
            screenshot_path = str(Path(DOWNLOAD_PATH)/"screenshots"/"schedule_screenshot.png")

            await self.tab.waitForFunction('el => document.body.contains(el)', {"polling":"mutation"}, tbody)

            await tbody.screenshot(
                options={
                    "path":screenshot_path 
                }
            )
            response['success'] = True
            response['data']['schedule']['type'] = 'screenshot'
            response['data']['schedule']['content'] = screenshot_path
        else:
            rows:list[ElementHandle] = (await tbody.querySelectorAll("tr"))[1:]
            data = [f"№ | {"ПРЕДМЕТ".center(33)} | {"ВРЕМЯ, КАБ.".center(23)} | Д/З"]
            for row in rows:
                les_num:str = await self.get_element_text(await row.querySelector('td.num_subject'))
                les_name:str = await self.get_element_text(await row.querySelector('* > a.subject'))
                les_task:str = await self.get_element_text(await row.querySelector('* > div.three_dots'))
                les_time_room:str = await self.get_element_text(await row.querySelector('* > div.time'))

                text = f"{les_num} | {les_name.center(34)} | {les_time_room.center(23)} | {les_task}"
                data.append(text)

            output_string = f'\n\n{"="*45}\n\n'.join(data)

            response['success'] = True
            response['data']['schedule']['type'] = 'text'
            response['data']['schedule']['content'] = output_string

        paperclips = (await tbody.querySelectorAll("i.mdi-paperclip"))
        logger.info(f"Paperclips found: {len(paperclips)}")
        if len(paperclips)>0:
            await self.tab.evaluate(f"""
            (el) => {{
                el.querySelectorAll("i.mdi-paperclip").forEach(paperclip => paperclip.click());                   
            }}""", tbody); logger.info("Paperclips clicked")

            await self.tab.waitForFunction(f"""(el)=> {{
                return el.querySelectorAll('div.attachments div.attach>a').length>0;
            }}""", {'timeout':5000}, tbody); logger.info("Waiting for a's")

            # file_names:set[str] = set(await self.tab.evaluate(f"""(el)=>{{
            #     const texts = [];
            #     const links = el.querySelectorAll('div.attachments div.attach > a');
            #     links.forEach((attachment, index) => {{
            #         attachment.click();
            #         texts.push(attachment.querySelector('div.name_file').innerText);
            #     }});
            #     return texts;
            # }}""", tbody))

            attachment_links = await tbody.querySelectorAll('div.attachments div.attach > a')
            file_names = set()

            for link in attachment_links:
                name_div = await link.querySelector('div.name_file')
                if name_div:
                    name = await self.tab.evaluate('(el) => el.innerText', name_div)
                    file_names.add(name)

                await self.tab.evaluate('(el) => el.click()', link)
                await asyncio.sleep(0.05)  

            # client = self.tab._client

            # expression = """
            # (el) => {
            #     const links = el.querySelectorAll('div.attachments div.attach > a');
            #     links.forEach(a => a.click());
            #     return [...links].map(a => a.querySelector('div.name_file').innerText);
            # }
            # """

            # result = await client.send('Runtime.evaluate', {
            #     'expression': f'({expression})(arguments[0])',
            #     'arguments': [{'objectId': tbody._remoteObject["objectId"]}],
            #     'returnByValue': True,
            #     'awaitPromise': True,
            #     'userGesture': True
            # })

            # file_names = set(result.get('result', {}).get('value', []))

            
            files_paths = [str(Path(DOWNLOAD_PATH)/"files"/str(file_name)) for file_name in file_names]
            response['data']['schedule']['files'] = files_paths

            while True:
                list_dir = await FilesManager.list_dir(Path(DOWNLOAD_PATH)/"files")
                downloaded_files = [file for file in list_dir if not file.endswith(".crdownload")]
                logger.info(f"Waiting for downlad files: {len(downloaded_files)}/{len(file_names)} | file_names = {file_names}")
                if len(downloaded_files) >= len(file_names) and (not any(file.endswith(".crdownload") for file in list_dir)):
                    break
                await asyncio.sleep(0.5)
        return response

class HomePage(BasePage):

    #Selectors
    GO_TO_STUDENTIARY_BUTTON = 'a[ng-click="$ctrl.selectTab(tabItem)"]'

    def __init__(self, tab, user_data, user_id):
        super().__init__(tab, user_data, user_id)
        self.url = ""
    
    async def go_to_studentiary(self) -> StudentiaryPage:
        # await self.tab.waitForFunction(f'''() => {{
        #     const buttons = document.querySelectorAll('{HomePage.GO_TO_STUDENTIARY_BUTTON}');
        #     const target = buttons[8];
        #     return target && angular.element(target).scope();
        # }}''', timeout=5000)

        await self.tab.evaluate(f'''() => {{
            const button = document.querySelectorAll('{HomePage.GO_TO_STUDENTIARY_BUTTON}')[6].click();
        }}''')
        return StudentiaryPage(self.tab, self.user_data, self.user_id)

class LoginPage(BasePage):

    # Selectors
    SCHOOLS_SELECTOR = 'li.select2-results__option'
    SCHOOL_NAME_SPAN = "span.select2-selection__rendered"
    SCHOOL_NAME_INPUT = "input.select2-search__field"
    LOGIN_INPUT = "input[name=loginname]"
    PASSWORD_INPUT = "input[name=password]"
    LOGIN_BUTTON = "div.primary-button"
    SECURITY_SKIP_BUTTON = "button.btn-primary"

    def __init__(self, tab:Page, user_data:dict, user_id:int):
        super().__init__(tab, user_data, user_id)
        self.url:str = "https://e-school.obr.lenreg.ru/authorize/login"

    async def security_check(self) -> None:
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
                    'type':'Ошибка авторизации',
                    'message':'Неверный логин/пароль или отказано в доступе на сайт по другой, неизвестной причине.\n'
                },
                'data':{}
            }
            return response

        await self.security_check()
        return HomePage(self.tab, self.user_data, self.user_id)