import asyncio, os; os.system("cls")
from middlewares.browserManager import *

asyncio.get_event_loop().run_until_complete(BrowserManager.main())