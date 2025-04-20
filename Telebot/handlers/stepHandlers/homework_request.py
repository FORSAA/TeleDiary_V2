from Telebot.libs.handlerLibs import *
from Parser.middlewares.browserManager import BrowserManager
from Parser.middlewares.filesManager import FilesManager

months = {
    'январь': 'января', 'февраль': 'февраля', 'март': 'марта', 'апрель': 'апреля',
    'май': 'мая', 'июнь': 'июня', 'июль': 'июля', 'август': 'августа',
    'сентябрь': 'сентября', 'октябрь': 'октября', 'ноябрь': 'ноября', 'декабрь': 'декабря'
}

homework_request_router = Router()

@homework_request_router.callback_query(
    StateFilter(HomeworkRequest.selecting_day),
    F.data.startswith("date:")
)
async def handle_date(callback: CallbackQuery, state:FSMContext):
    await callback.answer()

    selected_date = callback.data.split(":")[1].split()
    day, month = selected_date[0], months[selected_date[1]]

    await state.update_data(day = f"{day} {month}")
    
    await state.set_state(HomeworkRequest.selecting_type)
    await telebotMiddlewares.render(callback, TypeSelectPage)


@homework_request_router.callback_query(
    StateFilter(HomeworkRequest.selecting_type),
    F.data.startswith("type:")
)
async def handle_type(callback:CallbackQuery, state:FSMContext):
    await callback.answer('')

    await state.update_data(type = callback.data.split(":")[1])
    
    await telebotMiddlewares.render(callback, AwaitPage)

    user_id = callback.from_user.id
    user:User = await telebotMiddlewares._get_user(user_id)

    request_data = await state.get_data()
    request_day:str = request_data['day']
    request_type:str = request_data['type']

    request = {
        'auth_data' : user.auth_data,
        'type' : request_type,
        'date' : request_day
    }

    if (request_type == 'screenshot'):
        await callback.message.bot.send_chat_action(user_id, ChatAction.UPLOAD_PHOTO)
    else:
        await callback.message.bot.send_chat_action(user_id, ChatAction.TYPING)

    await state.set_state(HomeworkRequest.awaiting_answer)

    response = await BrowserManager.get_homework(request, user_id)

    if response['success']:
        links = response['data']['links']
        files = response['data']['schedule']['files']
        response_type = response['data']['schedule']['type']
        response_content = response['data']['schedule']['content']
        if response_type=='screenshot':
            await bot.send_photo(user_id, FSInputFile(response_content))
            if links:
                await bot.send_message(user_id, ' | '.join(links))
        else:
            await bot.send_message(user_id, response_content)
        
        if files:
            media = []
            for file in files:
                media.append(InputMediaDocument(type='document', media=FSInputFile(file)))
            await bot.send_media_group(user_id, media=media)
        
        await FilesManager.clear_dir(f"temp/{user_id}/files", f"temp/{user_id}/screenshots")
    else:
        await bot.send_message(user_id, f"Во время выполнения запроса возникла ошибка '{response['error']['type']}'.\nТекст ошибки: {response['error']['message']}")
    await state.clear()
    await telebotMiddlewares.render(callback, StartPage)
