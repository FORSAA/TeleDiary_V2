from Telebot.libs.handlerLibs import *

any_message_router = Router()

@any_message_router.message(F)
async def any_message_handler(message:Message):
    await message.delete()