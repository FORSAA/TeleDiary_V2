from Telebot.libs.handlerLibs import *

cmd_start_router = Router()

@cmd_start_router.message(Command('start'))
async def cmd_start_handler(message:Message):
    user = await telebotMiddlewares._get_user(message.from_user.id)
    if not user.started:
        await bot.send_message(message.chat.id, 'Давайте начнем! Функционал бота описан в меню "Как пользоваться?". \n\nТакже, там вы можете посмотреть как начать взаимодействовать с ним и отправлять запросы.')
        user.started = True
    await telebotMiddlewares.render(message, StartPage)