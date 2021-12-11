"""the service model of bot

To use this model, there must be a parsed script. Developer


Typical usage example:
from parser import load_script


script = load_script(f)
bot = bot_module.BotModel()
bot.build_model(script)
"""
import importlib
import inspect

from enum import Enum, auto

from bot_service.service.model.exception import ConflictException


PREVIOUS_SECTION = "返回"
CANCEL_SCRIPT = "取消"
UNKNOWN_MSG = "祈蒙见恕！小二没理解少侠的意思..."


class CommandEnum(Enum):
    """the enumerate class to describe the type of command
    """
    Root = auto()
    Service = auto()
    Text = auto()
    Script = auto()
    ScriptWaiting = auto()
    FAQ = auto()
    KVItem = auto()
    Setting = auto()
    Any = auto()


class BotNode:  # one service, one node
    """the node data structure to store information
    """

    def __init__(self) -> None:
        """init

        It will define its private variables
        """
        self.__query = {}
        self.__faq_keyword = None
        self.__faq: dict[str, str] = {}

    def set_query(self, type: CommandEnum, q: str, *args) -> None:
        """set query command for text and script

        Args:
            type (CommandEnum): type of the script
            q (str): text for query to response

        Raises:
            ConflictException: text to be registered is already existed
        """
        if type not in {
            CommandEnum.Text,
            CommandEnum.Script,
            CommandEnum.ScriptWaiting
        }:
            raise Exception("illegal type of query.")
        if q in self.__query:
            raise ConflictException("keyword '%s' has conflict." % q)
        elif type == CommandEnum.ScriptWaiting:
            module = importlib.import_module(
                '.' + args[1], 'bot_service.service.model.module')
            if not inspect.isfunction(module.handle):
                raise Exception("%s.handle is not a function." % args[2])
            self.__query[q] = (type, args[0], module.handle)
        elif type == CommandEnum.Script:
            module = importlib.import_module(
                '.' + args[0], 'bot_service.service.model.module')
            if not inspect.isfunction(module.handle):
                raise Exception("%s.handle is not a function." % args[1])
            self.__query[q] = (type, module.handle)
        else:
            self.__query[q] = (type, args[0])

    def set_faq_keyword(self, s: str) -> None:
        """set the keyword to print the entire faq

        Args:
            s (str): the keyword

        Raises:
            ConflictException: faq keyword is already existed
        """
        if self.__faq_keyword is not None:
            raise ConflictException('faq keyword existed.')
        self.__faq_keyword = s

    def set_faq(self, q: str, a: str) -> None:
        """add an item to faq list

        Args:
            q (str): question
            a (str): answer
        """
        self.__faq[q] = a

    def get_query(self, q: str) -> None | tuple:
        """try to get an anwser from the query list

        Args:
            q (str): keyword

        Returns:
            tuple: (type, info ...) of the option
            None: not found
        """
        return self.__query.get(q)

    def get_all_faq(self) -> str:
        """get the merged entire faq as a string

        Returns:
            str: the faq string
        """
        faq = ""
        cnt = 0
        for k, v in self.__faq.items():
            cnt += 1
            if cnt > 1:
                faq += '\n'
            faq += f"{cnt}. {k}\n{v}"
        return faq

    def get_all_query_keys(self) -> list[tuple[CommandEnum, str]]:
        """get keyword list of the query list

        Returns:
            list[tuple[CommandEnum, str]]: the query keyword list
        """
        keys = []
        items = self.__query.items()
        for k, v in items:
            keys.append((v[0], k))
        return keys

    def get_faq_keyword(self) -> str | None:
        """get previously defined keyword of faq

        Returns:
            str: the keyword
            None: no keyword set previously
        """
        return self.__faq_keyword

    def search_faq(self, q: str) -> str | None:
        """search a question in faq list

        Args:
            q (str): question

        Returns:
            str: merged string of result items
            None: no result found
        """
        faq = ""
        cnt = 0
        for k, v in self.__faq.items():
            cnt += 1
            if q not in k:
                continue
            if cnt > 1:
                faq += '\n'
            faq += f"{cnt}. {k}\n{v}"
        if len(faq.strip()) == 0:
            return None
        return faq


class BotModel:
    """core model of bot system

    It will create a automator from user defined script. The script passed
    here should be parsed and well verified.
    """

    class StatType(Enum):
        """the enumerate class to describe the stat in automator
        """
        Root = 0
        Serv = 1
        Wait = 2

    def __init__(self) -> None:
        """init

        It will define its private variables
        """
        self.__stat_table: list[dict] = []
        self.__node_list: list[BotNode] = []
        self.__setting: dict[str, str] = {}

    def build_model(self, script: list) -> None:
        """to parse the script and generate an automator of the bot

        Args:
            script (list): the parsed script
        """
        def load_setting(setting: list[tuple]):
            for (_, k, v), _ in setting:
                self.__setting[k] = v

        def recursive_build(command: tuple[tuple, list | None]):
            """the function to generate the transition table of the automator

            Args:
                command (tuple[tuple, list): the root command of a low level
                code block
            """
            node = BotNode()
            self.__node_list.append(node)
            if command[0][0] == CommandEnum.Root:
                self.__stat_table.append({
                    'type': BotModel.StatType.Root,
                    'node': len(self.__node_list) - 1,
                    'wait': {},
                    'serv': {}
                })
            else:
                self.__stat_table.append({
                    'type': BotModel.StatType.Serv,
                    'node': len(self.__node_list) - 1,
                    'prev': len(self.__stat_table) - 1,
                    'wait': {},
                    'serv': {}
                })
            prev = len(self.__stat_table) - 1
            prev_node = len(self.__node_list) - 1

            for elem in command[1]:
                elem: tuple[CommandEnum, list | None]
                try:
                    if elem[0][0] == CommandEnum.Setting:
                        load_setting(elem[1])
                    elif elem[0][0] == CommandEnum.Service:
                        last = len(self.__stat_table) - 1
                        recursive_build(elem)
                        servs = self.__stat_table[prev]['serv']
                        if elem[0][1] in servs:
                            print("conflict in service names.")
                        servs[elem[0][1]] = last + 1
                    elif elem[0][0] == CommandEnum.ScriptWaiting:
                        self.__stat_table.append({
                            'type': BotModel.StatType.Wait,
                            'node': prev_node,
                            'token': elem[0][1],
                            'cancel': prev
                        })
                        self.__stat_table[prev]['wait'][elem[0][1]] = prev + 1
                        node.set_query(CommandEnum.ScriptWaiting,
                                       elem[0][1], elem[0][2], elem[0][3])
                    elif elem[0][0] == CommandEnum.Script:
                        node.set_query(CommandEnum.Script,
                                       elem[0][1], elem[0][2])
                    elif elem[0][0] == CommandEnum.Text:
                        node.set_query(CommandEnum.Text,
                                       elem[0][1], elem[0][2])
                    elif elem[0][0] == CommandEnum.FAQ:
                        node.set_faq_keyword(elem[0][1])
                        for ((_, q, a), _) in elem[1]:
                            node.set_faq(q, a)
                except Exception as e:
                    print(e)

        recursive_build(((CommandEnum.Root, ), script))

    def handle_message(self, stat: int, msg: str = None) -> tuple[int, list[str]]:
        """handling an user message to generate the response and next stat

        Args:
            stat (int): the user's stat now
            msg (str, optional): user's message. Defaults to None (means root).

        Returns:
            tuple[int, list[str]]: (next_stat, [reply1, reply2, ...])
        """
        def enter_node(stat: int, node: BotNode) -> str:
            """generate the welcome message of entering a service or the root

            Args:
                stat (int): the user's stat now
                node (BotNode): the node (service or root) to enter

            Returns:
                str: welcome message
            """
            reply = "以下是本庄可以提供的选项~\n"
            service = list(self.__stat_table[stat]['serv'].keys())
            question = []
            for _, k in node.get_all_query_keys():
                question.append(k)
            if (faq_kw := node.get_faq_keyword()) is not None:
                question.append(faq_kw)
            if len(service) > 0:
                reply += '\n'.join(["子服务："] + service) + '\n'
            if len(question) > 0:
                reply += '\n'.join(["服务选项："] + question) + '\n'
            reply += "如果有其它问题也可以直接和我讲~"
            return reply

        if msg is None and stat == 0:  # root
            return (stat, [enter_node(stat, self.__node_list[0]) + f"\n在子服务输入{PREVIOUS_SECTION}可以返回上一级~"])

        replies = []
        stat_properties = self.__stat_table[stat]
        type = stat_properties['type']
        match type:
            case BotModel.StatType.Wait:
                if msg == CANCEL_SCRIPT:
                    replies.append("取消成功~")

                    stat = stat_properties['cancel']
                else:
                    arg = msg  # the msg is an argument

                    token = stat_properties['token']
                    node = self.__node_list[stat_properties['node']]
                    handle = node.get_query(token)[2]
                    try:
                        reply = handle(arg)
                    except:
                        reply = "未知错误"
                    stat = stat_properties['cancel']
                    replies.append(reply)
            case BotModel.StatType.Serv | BotModel.StatType.Root:
                if type == BotModel.StatType.Serv and msg == PREVIOUS_SECTION:
                    replies.append("返回成功~")

                    stat = stat_properties['prev']
                    stat_properties = self.__stat_table[stat]
                    node = self.__node_list[stat_properties['node']]

                    replies.append(enter_node(stat, node))
                else:
                    node = self.__node_list[stat_properties['node']]
                    if msg in stat_properties['serv']:
                        stat = stat_properties['serv'][msg]
                        stat_properties = self.__stat_table[stat]
                        next_node = self.__node_list[stat_properties['node']]

                        replies.append(enter_node(stat, next_node))
                    elif msg in stat_properties['wait']:
                        replies.append(node.get_query(msg)[1] + '\n')
                        replies.append(f"输入{CANCEL_SCRIPT}可以放弃操作~")

                        stat = stat_properties['wait'][msg]
                    elif (query := node.get_query(msg)) is not None:
                        match query[0]:
                            case CommandEnum.Text:
                                replies.append(query[1])
                            case CommandEnum.Script:
                                handle = query[1]
                                try:
                                    reply = handle()
                                except:
                                    reply = "未知错误"
                                replies.append(reply)
                    elif msg == node.get_faq_keyword():
                        replies.append(node.get_all_faq())
                    elif (faq := node.search_faq(msg)) is not None:
                        replies.append(faq)
                    else:
                        replies.append(UNKNOWN_MSG)
        return (stat, replies)
