from Telebot.libs.handlerLibs import *
from datetime import datetime

week_page_router = Router()

@week_page_router.callback_query(lambda call: call.data=="get_homework")
async def get_homework_cal_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(HomeworkRequest.selecting_day)
    page = telebotMiddlewares._generate_week_select_page(datetime.today())
    await telebotMiddlewares.render(callback, page, row_width=3)
    
@week_page_router.callback_query(lambda call: call.data.startswith("week:"))
async def change_week(callback: CallbackQuery):
    date = datetime.strptime(callback.data.split(":")[1], "%Y-%m-%d")
    page = telebotMiddlewares._generate_week_select_page(date)
    print(page.markup_data, page.message_text)
    await telebotMiddlewares.re_render(callback, page, row_width=3)


@week_page_router.callback_query(F.data.startswith("date:"))
async def handle_date(callback: CallbackQuery):
    selected_date = datetime.strptime(callback.data.split(":")[1], "%Y-%m-%d")
    await callback.message.answer(f"Вы выбрали дату: {selected_date.strftime('%d %B')}")
    await callback.answer()