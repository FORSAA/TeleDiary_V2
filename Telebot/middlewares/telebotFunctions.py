from Telebot.libs.telebotMiddlewareLibs import *

class telebotMiddlewares:
    @staticmethod
    async def render(data:Message | CallbackQuery, page: Page, del_prev=True, del_user_prev = True) -> None:
        user_id: int = data.from_user.id

        local_bot_last_message: None | Message = None
        local_user_last_message: None | Message = None

        if (user_id not in states)