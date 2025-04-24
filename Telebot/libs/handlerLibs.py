from aiogram.types import Message, CallbackQuery, InputMediaDocument, InputMediaPhoto, FSInputFile, InputMedia
from aiogram.filters import Filter, StateFilter, Command, CommandStart
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.state import State, StatesGroup 
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from aiogram import Router, F
from main import states, bot
import asyncio, logging

from Telebot.classes.templates.PageClassTemplates import *
from Telebot.classes.templates.UserClassTemplate import *
from Telebot.classes.states.authEditClass import *
from Telebot.classes.states.homeworkRequestClass import *
from Telebot.middlewares.telebotFunctions import telebotMiddlewares
