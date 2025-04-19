from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from Telebot.classes.templates.PageClassTemplates import Page
from Telebot.classes.templates.UserClassTemplate import User
from Parser.middlewares.filesManager import FilesManager
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from main import states, bot
import aiogram.exceptions
import os, aiogram