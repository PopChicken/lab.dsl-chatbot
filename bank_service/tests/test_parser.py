import logging
import unittest

import bot_service.service.model.parser as parser

from bot_service.service.model.bot import CommandEnum


class TestParser(unittest.TestCase):
    class __Capture:
        def __init__(self) -> None:
            self.__buffer = []
        
        def write(self, s: str) -> None:
            self.__buffer.append(s)
        
        def getline(self) -> str:
            return self.__buffer.pop(0)
        
        def getall(self) -> list[str]:
            buffer = self.__buffer
            self.__buffer = []
            return buffer

    def test_complicated(self) -> None:
        logger = logging.getLogger()
        logger.disabled = True
        with open('tests/testcase/complicated.def', 'r', encoding='utf8') as f:
            script = parser.load_script(f)
            
            assert script is not None
            assert script[0][0][0] == CommandEnum.Setting

            settings = script[0][1]
            assert len(settings) == 13
            assert settings[0] == ((CommandEnum.KVItem, 'name', 'name'), None)
            assert settings[12] == ((CommandEnum.KVItem, 'unkown', 'unkown'), None)
            
            assert script[1][0] == (CommandEnum.Service, 'service1')
            
            services = script[1][1]
            assert len(services) == 6
            assert services[0] == ((CommandEnum.Text, 'text test1', 'text1'), None)
            assert services[1] == ((CommandEnum.Script, 'script test1', 'script1'), None)

            assert services[4][0] == (CommandEnum.FAQ, 'faq1')
            
            faq = services[4][1]
            assert len(faq) == 8
            assert faq[0] == ((CommandEnum.KVItem, 'faq test1', 'answer1'), None)
            assert faq[7] == ((CommandEnum.KVItem, 'faq test8', 'answer8'), None)

            assert script[2][0] == (CommandEnum.Service, 'service2')
            
            services = script[2][1]
            assert len(services) == 6
            assert services[0] == ((CommandEnum.Text, 'text test4', 'test4'), None)
            assert services[2] == ((CommandEnum.Text, 'text test6', 'test6'), None)
            assert services[4] == ((CommandEnum.ScriptWaiting, 'script test2', 'holder', 'script2'), None)
            assert services[5] == ((CommandEnum.Script, 'script test3', 'script3'), None)
            
            assert services[3][0] == (CommandEnum.Service, 'service3')
            
            services = services[3][1]
            assert len(services) == 2
            assert services[0] == ((CommandEnum.Text, 'text test7', 'test7'), None)

            assert services[1][0] == (CommandEnum.FAQ, 'faq2')
            
            faq = services[1][1]
            assert len(faq) == 3
            assert faq[0] == ((CommandEnum.KVItem, 'faq test9', 'answer9'), None)
            assert faq[2] == ((CommandEnum.KVItem, 'faq test11', 'answer11'), None)
        
    def test_empty(self) -> None:
        logger = logging.getLogger()
        logger.disabled = True
        with open('tests/testcase/empty.def', 'r', encoding='utf8') as f:
            script = parser.load_script(f)

            assert script is not None
            assert isinstance(script, list)
            assert len(script) == 0
    
    def test_incorrect(self) -> None:
        logger = logging.getLogger()
        logger.handlers.clear()  # remove all the handlers
        logger.filters.clear()  # remove all the filters
        logger.propagate = False  # do not pass msg to the father logger
        # add a handler for test
        handler = logging.StreamHandler()
        capture = TestParser.__Capture()
        handler.setStream(capture)
        logger.addHandler(handler)
        logger.disabled = False  # enable logger
        with open('tests/testcase/incorrect.def', 'r', encoding='utf8') as f:
            parser.load_script(f)
            output = [s.strip() for s in capture.getall()]
            assert 'bad indentation at line 8.' in output
            assert 'sub-command not allowed at line 1.' in output
            assert 'syntax error at line 3.' in output
            assert 'sub-command not allowed at line 3.' in output
            assert 'no sub definition allowed under command at line 12.' in output
    
    def test_naughty_indent(self):
        logger = logging.getLogger()
        logger.disabled = True
        with open('tests/testcase/naughty_indent.def', 'r', encoding='utf8') as f:
            script = parser.load_script(f)
            
            assert script is not None
            
            assert script[0][0] == (CommandEnum.Service, 'service1')
            assert script[1][0] == (CommandEnum.Service, 'service2')
            
            services = script[0][1]
            assert len(services) == 3
            assert services[0] == ((CommandEnum.Text, 'text test1', 'text1'), None)
            assert services[1] == ((CommandEnum.Script, 'script test1', 'script1'), None)
            assert services[2][0] == (CommandEnum.FAQ, 'faq1')
            
            faq = services[2][1]
            assert len(faq) == 3
            assert faq[0] == ((CommandEnum.KVItem, 'faq test1', 'answer1'), None)
            assert faq[2] == ((CommandEnum.KVItem, 'faq test3', 'answer3'), None)
            
            services = script[1][1]
            assert len(services) == 2
            assert services[0] == ((CommandEnum.Text, 'text test4', 'text4'), None)
            assert services[1] == ((CommandEnum.Script, 'script test2', 'script2'), None)

    def test_recursive(self):
        logger = logging.getLogger()
        logger.disabled = True
        with open('tests/testcase/recursive.def', 'r', encoding='utf8') as f:
            script = parser.load_script(f)
            
            assert script is not None
            
            assert script[0][0] == (CommandEnum.Service, '1')
            
            services = script[0][1]
            assert len(services) == 1
            assert services[0][0] == (CommandEnum.Service, '2')
            
            services = services[0][1]
            assert len(services) == 1
            assert services[0][0] == (CommandEnum.Service, '3')

            services = services[0][1]
            assert len(services) == 1
            assert services[0][0] == (CommandEnum.Service, '4')

            services = services[0][1]
            assert len(services) == 1
            assert services[0][0] == (CommandEnum.Service, '5')
