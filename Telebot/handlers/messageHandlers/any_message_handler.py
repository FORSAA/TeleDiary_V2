from Telebot.libs.handlerLibs import *

any_message_router = Router()

@any_message_router.message(F)
async def any_message_handler(message:Message):
    await message.delete()
    user = states[message.from_user.id]
    print(
    f"""
    {"DEBUG".center(41, "=")}

    - User.auth_state = {user.auth_state};
    - User.auth_data = {user.auth_data};
    - User.menu_state = {user.menu_state};

    {"".center(41, "=")}
    """
    )