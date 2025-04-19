from Telebot.libs.telebotMiddlewareLibs import *

class telebotMiddlewares:
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
    async def render(data:Message | CallbackQuery, page: Page, del_prev=True, del_user_prev = True) -> None:
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
        
        sent_message = await bot.send_message(chat_id=user_id, text=page.message_text, reply_markup=page.get_markup(), parse_mode="HTML")

        user.menu_state = page.name
        user.bot_last_message = sent_message