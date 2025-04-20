from aiogram import Router
from .messageHandlers import messageRouters
from .callbackHandlers import callbackRouter
from .stepHandlers.auth_data_edit_handler import auth_data_edit_router
from .stepHandlers.homework_request import homework_request_router

handlersRouters = Router()
handlersRouters.include_routers(homework_request_router, auth_data_edit_router, messageRouters, callbackRouter)