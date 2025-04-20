from Telebot.libs.handlerLibs import *
from datetime import datetime
import copy

week_page_router = Router()

@week_page_router.callback_query(lambda call: call.data=="get_homework")
async def get_homework_cal_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')

    user: User = await telebotMiddlewares._get_user(callback.from_user.id)
    
    if not user.auth_state:
        page = copy.deepcopy(BlankPage)
        page.message_text = (
            'Ошибка! Вы не авторизованы!\n\n'
            'Перейдите на страницу авторизации, заполните данные и повторите попытку!'
        )
        await telebotMiddlewares.render(callback, page)
        return
    
    await state.set_state(HomeworkRequest.selecting_day)
    page = telebotMiddlewares._generate_week_select_page(datetime.today())
    await telebotMiddlewares.render(callback, page, row_width=3)
    
@week_page_router.callback_query(
        StateFilter(HomeworkRequest.selecting_day),
        lambda call: call.data.startswith("week:")
        )
async def change_week(callback: CallbackQuery):
    date = datetime.strptime(callback.data.split(":")[1], "%Y-%m-%d")
    page = telebotMiddlewares._generate_week_select_page(date)
    await telebotMiddlewares.re_render(callback, page, row_width=3)
