"""load script to build a bot easily
"""
import logging
import os

import bot_service.service.model.bot as bot_module

from bot_service.service.model.parser import load_script


bots: dict[str, bot_module.BotModel] = {}

def __load_definition(path: str) -> None:
    logger = logging.getLogger()
    try:
        with open(path, 'r', encoding='utf8') as f:
            script = load_script(f)
    except:
        return

    if script is not None:
        bot = bot_module.BotModel()
        success = bot.build_model(script)
        if success:
            bots[str(len(bots))] = bot
        else:
            logger.warn("fail to load '%s'." % path)


__walk = os.walk('bot_service/definition')

for root, _, files in __walk:
    for name in files:
        if len(name) < 4 or name[-4:] != '.def':
            continue
        __load_definition(f'{root}/{name}')