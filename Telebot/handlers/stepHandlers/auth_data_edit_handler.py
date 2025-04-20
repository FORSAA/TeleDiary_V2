from Telebot.libs.handlerLibs import *

auth_data_edit_router = Router()

@auth_data_edit_router.callback_query(StateFilter(None), lambda call: call.data=="auth_data_edit")
async def cal_auth_data_edit(call: CallbackQuery, state: FSMContext):
    await call.answer('')

    user = await telebotMiddlewares._get_user(call.from_user.id)
    
    await telebotMiddlewares.render(call, AuthDataEditPage)
    await state.set_state(AuthEdit.changing_login)

@auth_data_edit_router.message(
    AuthEdit.changing_login
)
async def login_sent(message: Message, state: FSMContext):
    await state.update_data(login = message.text)

    user = await telebotMiddlewares._get_user(message.chat.id)
    await user.bot_last_message.delete()
    
    await message.delete()
    user.bot_last_message = await message.answer('Логин принят! Введите пароль.')
    
    await state.set_state(AuthEdit.changing_password)

@auth_data_edit_router.message(
    AuthEdit.changing_password
)
async def password_sent(message: Message, state: FSMContext):
    await state.update_data(password = message.text)

    user = await telebotMiddlewares._get_user(message.chat.id)
    await user.bot_last_message.delete()

    user_data = await state.get_data()
    await state.clear()

    login = user_data['login']
    password = user_data['password']

    await message.delete()
    user.bot_last_message = await message.answer(
        f'Данные авторизации приняты! Сохранены следующие данные для авторизации: {login} : {password}!\n\n'
        f'Выходим в главное меню . . .'
    )

    user.auth_state = True
    user.auth_data = {
        'login':login,
        'password':password
    }

    await asyncio.sleep(2)
    await telebotMiddlewares.render(message, StartPage) #, del_user_prev=False
