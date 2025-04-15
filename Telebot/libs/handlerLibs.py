from aiogram.types import Message, CallbackQuery, InputMediaDocument, InputMediaPhoto, FSInputFile, InputMedia
from aiogram.filters import Filter, StateFilter, Command, CommandStart
from aiogram.fsm.state import State, StatesGroup 
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from aiogram import Router, F
from main import states
import asyncio

from Telebot.classes.templates.PageClassTemplates import *