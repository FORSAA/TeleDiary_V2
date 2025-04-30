from Telebot.libs.telebotMiddlewareLibs import *

class telebotMiddlewares:
    @staticmethod
    def _get_week_dates(reference: datetime):
        monday = reference - timedelta(days=reference.weekday())
        return [monday+timedelta(days=i) for i in range(6)]
        
    @staticmethod
    def _generate_week_select_page(week_ref: datetime) -> Page:
        dates = telebotMiddlewares._get_week_dates(week_ref)
        
        buttons = [
            InlineKeyboardButton(
                text=f"{d.strftime('%B')}, {d.day}-е",
                callback_data=f"date:{d.strftime('%e %B').lower()}"
            )
            for d in dates
        ]

        nav_buttons = [
            InlineKeyboardButton(text="<<<", callback_data=f"week:{(week_ref - timedelta(days=7)).strftime('%Y-%m-%d')}"),
            InlineKeyboardButton(text=" ", callback_data="-"),
            InlineKeyboardButton(text=">>>", callback_data=f"week:{(week_ref + timedelta(days=7)).strftime('%Y-%m-%d')}")
        ]

        return Page(
            name='week_select_page',
            message_text='Выберите дату, которая вас интересует:',
            markup_data=buttons + nav_buttons + [
                InlineKeyboardButton(text='« Вернуться в главное меню', callback_data='menu')
            ]
        )
    
    @staticmethod
    async def _get_user(user_id: int) -> User:
        if user_id not in states:
            await FilesManager.make_dir(
                ("temp", f"{user_id}"),
                (f"temp\\{user_id}", "files"),
                (f"temp\\{user_id}", "screenshots")
            )
            states[user_id] = User(
                    {
                        'docs_path':f'temp\\{user_id}\\files',
                        'screenshots_path':f'temp\\{user_id}\\screenshots'
                    }
                )
        return states[user_id]
    
    @staticmethod
    async def render(data:Message | CallbackQuery, page: Page, del_prev: bool = True, del_user_prev: bool = True, row_width:int = 2, extra_text:str = '') -> None:
        user_id = data.from_user.id
        user: User = await telebotMiddlewares._get_user(user_id)

        incoming_message: Message = data.message if isinstance(data, CallbackQuery) else data
                
        if del_prev and user.bot_last_message:
            try:
                await bot.delete_message(user_id, user.bot_last_message.message_id)
            except:
                pass
        
        if del_user_prev:
            try:
                await bot.delete_message(user_id, incoming_message.message_id)
            except:
                pass
        
        sent_message = await bot.send_message(chat_id=user_id, text=page.message_text + extra_text, reply_markup=page.get_markup(row_width), parse_mode="HTML")

        user.menu_state = page.name
        user.bot_last_message = sent_message

    @staticmethod
    async def re_render(data: Message | CallbackQuery, page: Page, row_width:int = 2):
        message: Message = data.message if isinstance(data, CallbackQuery) else data

        await message.edit_text(
            text=page.message_text,
            reply_markup=page.get_markup(row_width)
        )

        if isinstance(data, CallbackQuery):
            await data.answer('')