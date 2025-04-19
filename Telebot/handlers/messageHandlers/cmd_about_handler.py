from Telebot.libs.handlerLibs import *

cmd_about_router = Router()

@cmd_about_router.message(Command('about'))
async def cmd_about_handler(message:Message):
    await telebotMiddlewares.render(message, AboutPage)