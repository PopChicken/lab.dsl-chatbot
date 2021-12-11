"""the module to parse a file to bot readable script

a simple interpreter to parse the bot defination script,
built based on recursive descend analysis.

Typical usage:
script = load_script(f)
"""
import logging

from typing import IO

from pyparsing import Suppress, Regex, Combine, Word, nums, ParserElement, ParseResults
from pyparsing.exceptions import ParseException

from bot_service.service.model.bot import CommandEnum


__quote = Suppress('"')
__content_quoted = __quote + Regex(r'[^"]*') + __quote
__service = Suppress('service') + __content_quoted
__text = Suppress('text') + __content_quoted + __content_quoted
__script = Suppress('script') + __content_quoted + __content_quoted
__script_wating = Suppress('script') + __content_quoted + __content_quoted + __content_quoted
__faq = Suppress('faq') + __content_quoted
__faq_item = __content_quoted + Suppress(':') + __content_quoted
__setting = Suppress('settings')

__logger = logging.getLogger()


cmd_mapping = {
    CommandEnum.Root: {
        CommandEnum.Setting,
        CommandEnum.Service
    },
    CommandEnum.Setting: {
        CommandEnum.KVItem
    },
    CommandEnum.Service: {
        CommandEnum.Service,
        CommandEnum.Text,
        CommandEnum.Script,
        CommandEnum.ScriptWaiting,
        CommandEnum.FAQ
    },
    CommandEnum.FAQ: {
        CommandEnum.KVItem
    },
    CommandEnum.Any: {
        CommandEnum.Service,
        CommandEnum.Text,
        CommandEnum.Script,
        CommandEnum.ScriptWaiting,
        CommandEnum.FAQ,
        CommandEnum.KVItem
    }
}


def identify_command(s: str) -> tuple | None:
    """try to indentify a command
    
    Args:
        s (str): command string
    
    Returns:
        tuple: (type, info ...)
        None: not indentified
    """
    def safe_parse(pattern: ParserElement, s: str) -> ParseResults | None:
        """parse a command string safely with no exception interruption

        Returns:
            ParseResult: the parse result
            None: not matched
        """
        try:
            result = pattern.parse_string(s, parse_all=True)
        except ParseException:
            return None
        return result

    if (r := safe_parse(__service, s)) is not None:
        return (CommandEnum.Service, r[0])
    elif (r := safe_parse(__text, s)) is not None:
        return (CommandEnum.Text, r[0], r[1])
    elif (r := safe_parse(__script_wating, s)) is not None:
        return (CommandEnum.ScriptWaiting, r[0], r[1], r[2])
    elif (r := safe_parse(__script, s)) is not None:
        return (CommandEnum.Script, r[0], r[1])
    elif (r := safe_parse(__faq, s)) is not None:
        return (CommandEnum.FAQ, r[0])
    elif (r := safe_parse(__faq_item, s)) is not None:
        return (CommandEnum.KVItem, r[0], r[1])
    elif (r := safe_parse(__setting, s)) is not None:
        return (CommandEnum.Setting, )
    else:
        return None


def analyze(lines: list[str]) -> list:
    """parsing the user defined script, returning well formatted script structure
    
    First, converting the indentation to code block with space lines
    skipped. If there are some incorrect intendation, the analysis fails.
    Second, synatic analysis will be performed, using the recursive 
    descent analysis. It tries to identify all the lines to commands
    defined in this module. If there are some lines cannot be identified
    or appear at some incorrect code block, the analysis fails.
    
    Args:
        lines (list[str]): raw user script lines
    
    Returns:
        list: formatted script object (list)
    """    
    def recursive_analyze(head_type: CommandEnum, raw_struct: list[tuple[int, str] | list]) -> list[tuple] | None:
        """recursive descent analysis

        Args:
            head_type (CommandEnum): the father command of this block,
            determining the allowed commands.
            raw_struct (list[tuple[int, str] | list]): list of elements.
            an element can be (line, string) or list (sub-block).

        Returns:
            list[tuple]: parsed commands
            None: failed
        """
        fail_flag = False
        script = []
        cur = 0
        for cur in range(0, len(raw_struct)):
            elem = raw_struct[cur]
            
            if cur == len(raw_struct) - 1:
                next_elem = None
            else:
                next_elem = raw_struct[cur + 1]
            
            if isinstance(elem, list):
                continue

            if (command := identify_command(elem[1])) is None:
                __logger.error("syntax error at line %d." % elem[0])
                fail_flag = True
                cmd_type = CommandEnum.Any
            else:
                cmd_type = command[0]
            
            # if no syntas error, check sub-command
            field = cmd_mapping.get(head_type)
            if field is not None and cmd_type not in field:
                fail_flag = True
                __logger.error("sub-command not allowed at line %d." % elem[0])

            sub_script = None
            if isinstance(next_elem, list):
                if cmd_type == CommandEnum.Any or cmd_type not in cmd_mapping:
                    __logger.error("no sub defination allowed under command at line %d." % (elem[0] + 1))
                    fail_flag = True

                sub_script = recursive_analyze(cmd_type, next_elem)
                if sub_script is None:
                    fail_flag = True
            script.append((command, sub_script))

        if fail_flag:
            return None
        return script
        
    fail_flag = False
    
    # step 1: convert indentation to structural script
    stack = [(0, [])]
    line_cnt = 0

    for line in lines:
        line_cnt += 1
        
        if len(line.strip()) == 0:
            continue

        level = len(line) - len(line.lstrip(' '))
        stack_peek: tuple[int, list] = stack[-1]
        top_level: int = stack_peek[0]
        top_script: list = stack_peek[1]

        if level == top_level:  # same level
            top_script.append((line_cnt, line.strip()))
        elif level > top_level:  # sub code block
            sub_script = [(line_cnt, line.strip())]
            top_script.append(sub_script)
            stack.append((level, sub_script))
        else:  # outside block
            index = len(stack)
            
            while True:
                # scan the stack. find the position
                # to recover when failed
                index -= 1
                stack_peek: tuple[int, list] = stack[index]
                if stack_peek[0] < level:
                    fail_flag = True  # bad indentation
                    __logger.error("bad indentation at line %d." % line_cnt)
                    break
                if stack_peek[0] > level:
                    continue

                stack_peek[1].append((line_cnt, line.strip()))
                stack = stack[:index + 1]  # apply changes
                break

    # step 2: syntactic analysis
    raw_struct = stack[0][1]
    del stack
    script = recursive_analyze(CommandEnum.Root, raw_struct)
    
    if fail_flag or script is None:
        __logger.warn("analysis failed.")
        return None

    return script


def load_script(f: IO) -> list:
    """try to parse a file stream to a bot model builder readable script

    Args:
        f (IO): fp

    Returns:
        list: parsed script, accepting by bot model builder 
    """
    lines = f.readlines()
    script = analyze(lines)
    
    if script is None:
        return None

    return script

