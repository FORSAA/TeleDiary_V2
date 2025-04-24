import logging
from Telebot.libs.handlerLibs import *
from Parser.middlewares.browserManager import BrowserManager
from Parser.middlewares.filesManager import FilesManager

logger = logging.getLogger("requests")
logger.setLevel(logging.INFO)
# logger.propagate = False

RESTRICTED_DOC = (".webp")

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

    logger.info(f"REQUEST BY: {user_id} | Day: {request_day} | Type: {request_type}")
    
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

    logger.info(f"REQUEST by USER #{user_id} WAS COMPLETED. SUCCESS: {response['success']}")

    if response['success']:
        links = response['data']['links']
        files = response['data']['schedule']['files']
        response_type = response['data']['schedule']['type']
        response_content = response['data']['schedule']['content']
        logger.info(f"RESPONSE CONTENT | Response_type: {response_type} | Response_content: {response_content} | Links: {links} | Files: {files}")
        if response_type=='screenshot':
            await bot.send_photo(user_id, FSInputFile(response_content))
            if links:
                await bot.send_message(user_id, 'Дополнительные ссылки:\n▹ '+'\n▹ '.join(set(links)))
        else:
            await bot.send_message(user_id, f'<pre>{response_content}</pre>', parse_mode="HTML")
        
        if files:
            files: list[str] = [file for file in files if not file.lower().endswith(RESTRICTED_DOC)]
            media_items = [
                InputMediaDocument(media=FSInputFile(path=file_path))
                for file_path in files
            ]
            for i in range(0, len(media_items), 9):
                chunk = media_items[i : i + 9]
                await bot.send_media_group(chat_id=user_id, media=chunk)
                await asyncio.sleep(1)
        
        await FilesManager.clear_dir(f"temp/{user_id}/files", f"temp/{user_id}/screenshots")
    else:
        await bot.send_message(user_id, f"Во время выполнения запроса возникла ошибка '{response['error']['type']}'.\nТекст ошибки: {response['error']['message']}")
    await state.clear()
    await telebotMiddlewares.render(callback, StartPage)
