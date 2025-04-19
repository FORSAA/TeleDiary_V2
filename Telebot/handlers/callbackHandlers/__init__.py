from aiogram import Router
from .get_menu_handler import get_menu_router
from .help_page_handler import help_page_router
from .de_auth_handler import de_auth_router

callbackRouter = Router()
callbackRouter.include_routers(get_menu_router, help_page_router, de_auth_router)