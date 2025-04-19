from Telebot.libs.handlerLibs import *

help_page_router = Router()

@help_page_router.callback_query(lambda call: call.data=='help_page')
async def help_page(call: CallbackQuery):
    await call.answer('')
    await telebotMiddlewares.render(call, HelpPage)