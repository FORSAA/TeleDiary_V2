from Telebot.libs.handlerLibs import *

get_menu_router = Router()

@get_menu_router.callback_query(lambda call: call.data == 'menu')
async def get_menu(call: CallbackQuery, state:FSMContext):
    await call.answer('')
    await state.clear()
    await telebotMiddlewares.render(call, StartPage)
