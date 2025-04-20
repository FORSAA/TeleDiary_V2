from pyppeteer.browser import Page
from pyppeteer.errors import TimeoutError
from pyppeteer.element_handle import ElementHandle
from datetime import datetime
from Parser.middlewares.filesManager import *
from Parser.middlewares.convert_to_full_date import *
from Parser.middlewares.get_object_id_from_date import *
import time
import asyncio
import re
import logging
