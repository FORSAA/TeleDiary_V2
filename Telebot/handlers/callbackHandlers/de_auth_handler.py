from Telebot.libs.handlerLibs import *

de_auth_router = Router()

@de_auth_router.callback_query(lambda call: call.data == 'de_auth')
async def help_page(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    await bot.delete_message(call.message.chat.id, states[call.from_user.id].bot_last_message.message_id)

    local_bot_last_message = await bot.send_message(call.message.chat.id, 'Ваши данные авторизации были отвязаны.\n\nВы будете возвращены в меню.')
    await asyncio.sleep(2)
    await local_bot_last_message.delete()
    await telebotMiddlewares.render(call, StartPage, del_last=False)

    states[call.from_user.id].auth_state = False
    states[call.from_user.id].auth_data = {}
    await state.clear()

