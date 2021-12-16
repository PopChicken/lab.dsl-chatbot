import logging
import unittest

import bot_service.service.model.parser as parser

from bot_service.service.model.bot import BotModel, CommandEnum


class TestBot(unittest.TestCase):

    def test_complicated(self) -> None:
        logger = logging.getLogger()
        logger.disabled = True

        script = [  # generated from complicated.def
            ((CommandEnum.Setting,), [
                ((CommandEnum.KVItem, 'name', 'name'), None),
                ((CommandEnum.KVItem, 'title', 'title'), None),
                ((CommandEnum.KVItem, 'welcome', 'welcome'), None),
                ((CommandEnum.KVItem, 'subservice', 'subservice'), None),
                ((CommandEnum.KVItem, 'option', 'option'), None),
                ((CommandEnum.KVItem, 'am', 'am'), None),
                ((CommandEnum.KVItem, 'pm', 'pm'), None),
                ((CommandEnum.KVItem, 'cancel', 'cancel'), None),
                ((CommandEnum.KVItem, 'cancel_success', 'cancel_success'), None),
                ((CommandEnum.KVItem, 'back', 'back'), None),
                ((CommandEnum.KVItem, 'back_success', 'back_success'), None),
                ((CommandEnum.KVItem, 'other', 'other'), None),
                ((CommandEnum.KVItem, 'unkown', 'unkown'), None)
            ]),
            ((CommandEnum.Service, 'service1'), [
                ((CommandEnum.Text, 'text test1', 'text1'), None),
                ((CommandEnum.Script, 'script test1', 'script1'), None),
                ((CommandEnum.Text, 'text test2', 'text2'), None),
                ((CommandEnum.Text, 'text test3', 'text3'), None), 
                ((CommandEnum.FAQ, 'faq1'), [
                    ((CommandEnum.KVItem, 'faq test1', 'answer1'), None),
                    ((CommandEnum.KVItem, 'faq test2', 'answer2'), None),
                    ((CommandEnum.KVItem, 'faq test3', 'answer3'), None),
                    ((CommandEnum.KVItem, 'faq test4', 'answer4'), None),
                    ((CommandEnum.KVItem, 'faq test5', 'answer5'), None),
                    ((CommandEnum.KVItem, 'faq test6', 'answer6'), None),
                    ((CommandEnum.KVItem, 'faq test7', 'answer7'), None),
                    ((CommandEnum.KVItem, 'faq test8', 'answer8'), None)
                ]),
                ((CommandEnum.Service, 'service4'), [
                    ((CommandEnum.Service, 'service5'), None),
                    ((CommandEnum.Service, 'service6'), None),
                    ((CommandEnum.Text, 'text test7', 'test7'), None),
                    ((CommandEnum.Text, 'text test8', 'test8'), None),
                    ((CommandEnum.Text, 'text test9', 'test9'), None)])
            ]),
            ((CommandEnum.Service, 'service2'), [
                ((CommandEnum.Text, 'text test4', 'test4'), None),
                ((CommandEnum.Text, 'text test5', 'test5'), None),
                ((CommandEnum.Text, 'text test6', 'test6'), None),
                ((CommandEnum.Service, 'service3'), [
                    ((CommandEnum.Text, 'text test7', 'test7'), None),
                    ((CommandEnum.FAQ, 'faq2'), [
                        ((CommandEnum.KVItem, 'faq test9', 'answer9'), None),
                        ((CommandEnum.KVItem, 'faq test10', 'answer10'), None),
                        ((CommandEnum.KVItem, 'faq test11', 'answer11'), None)
                    ])
                ]), 
                ((CommandEnum.ScriptWaiting, 'script test2', 'holder', 'script2'), None),
                ((CommandEnum.Script, 'script test3', 'script3'), None)
            ])
        ]

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
