"""load script to build a bot easily
"""
from . import bot as bot_module

from .parser import load_script


bot = None
__script = None
try:
    with open('bot_service/definition/script.def', 'r', encoding='utf8') as f:
        __script = load_script(f)
except:
    print('fail to load script.def.')
    exit(1)

if __script is not None:
    bot = bot_module.BotModel()
    bot.build_model(__script)