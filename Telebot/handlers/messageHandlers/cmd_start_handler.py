from Telebot.libs.handlerLibs import *

cmd_start_router = Router()

@cmd_start_router.message(Command('start'))
async def cmd_start_handler(message:Message):
    await telebotMiddlewares.render(message, StartPage)