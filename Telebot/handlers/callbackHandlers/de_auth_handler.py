from Telebot.libs.handlerLibs import *

de_auth_router = Router()

@de_auth_router.callback_query(lambda call: call.data == 'de_auth')
async def help_page(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    await state.clear()
    
    user:User = await telebotMiddlewares._get_user(call.from_user.id)
    user.auth_data = {}
    user.auth_state = False

    await bot.delete_message(call.message.chat.id, states[call.from_user.id].bot_last_message.message_id)

    local_bot_last_message = await bot.send_message(call.message.chat.id, 'Ваши данные авторизации были отвязаны.\n\nВы будете возвращены в меню.')
    await asyncio.sleep(2)
    await local_bot_last_message.delete()
    await telebotMiddlewares.render(call, StartPage, del_prev=False)


