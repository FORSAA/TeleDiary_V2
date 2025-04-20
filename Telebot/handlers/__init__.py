from aiogram import Router
from .messageHandlers import messageRouters
from .callbackHandlers import callbackRouter
from .stepHandlers.auth_data_edit_handler import auth_data_edit_router

handlersRouters = Router()
handlersRouters.include_routers(auth_data_edit_router, messageRouters, callbackRouter)