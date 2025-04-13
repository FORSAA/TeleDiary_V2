import asyncio, os, ast
from pyppeteer import *
import asyncstdlib as astd
from pyppeteer.browser import Browser
from middlewares.filesManager import FilesManager
from dotenv import load_dotenv; load_dotenv(".env")
from classes.Pages import *