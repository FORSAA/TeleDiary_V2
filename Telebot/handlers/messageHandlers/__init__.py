from aiogram import Router
from .cmd_start_handler import cmd_start_router
from .any_message_handler import any_message_router

messageRouters = Router()
messageRouters.include_routers(cmd_start_router, any_message_router)