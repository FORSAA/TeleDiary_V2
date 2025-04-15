from aiogram import Router
from .messageHandlers import messageRouters

handlersRouters = Router()
handlersRouters.include_routers(messageRouters)