from Telebot.libs.handlerLibs import *

any_callback_router = Router()

@any_callback_router.callback_query(lambda call: call.data)
async def any_callback_handler(callback: CallbackQuery):
    await callback.answer('')