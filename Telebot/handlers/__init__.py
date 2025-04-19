from aiogram import Router
from .messageHandlers import messageRouters
from .callbackHandlers import callbackRouter

handlersRouters = Router()
handlersRouters.include_routers(messageRouters, callbackRouter)