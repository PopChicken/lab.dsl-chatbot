import logging
import unittest

import bot_service.service.model.parser as parser

from bot_service.service.model.bot import BotModel, CommandEnum


class TestBot(unittest.TestCase):

    def test_complicated(self) -> None:
        logger = logging.getLogger()
        logger.disabled = True
        with open('tests/testcase/complicated.def', 'r', encoding='utf8') as f:
            script = parser.load_script(f)
            
        bot = BotModel()
        bot.build_model(script)

        stat, msg = bot.handle_message(0, "service1")
        assert len(msg) == 1
        assert msg[0] == 'welcome\nsubservice\nservice4\noption\ntext test1\ntext test2\ntext test3\nfaq1\nother'
        
        stat, msg = bot.handle_message(stat, "test2")
        assert len(msg) == 1
        assert msg[0] == '\n2. faq test2\nanswer2'
        
        stat, msg = bot.handle_message(stat, "back")
        assert len(msg) == 2
        assert msg[0] == 'back_success'
        assert msg[1] == 'welcome\nsubservice\nservice1\nservice2\nother'
        
        stat, msg = bot.handle_message(stat, "service2")
        assert len(msg) == 1
        assert msg[0] == 'welcome\nsubservice\nservice3\noption\ntext test4\ntext test5\ntext test6\nother'
        
        stat, msg = bot.handle_message(stat, "text test5")
        assert len(msg) == 1
        assert msg[0] == 'test5'
