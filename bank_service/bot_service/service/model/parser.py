from typing import IO

from pyparsing import Suppress, Regex, Combine, Word, nums, ParserElement, ParseResults
from pyparsing.exceptions import ParseException

from bot_service.service.model.bot import CommandEnum


quote = Suppress('"')
content_no_space = Regex(r'[^\s"]+')
content_no_space_semicolon = Regex(r'[^\s;"]+')
content_quoted = quote + Regex(r'[^"]*') + quote
content = content_quoted | content_no_space
number = Combine(Word(nums) + '.' + Word(nums)) | Word(nums)
any_no_quote = Regex(r'[^"]*')
integer = Word(nums)
service = Suppress('service') + content_quoted
text = Suppress('text') + content_quoted + content_quoted
script = Suppress('script') + content_quoted + content_quoted
script_wating = Suppress('script') + content_quoted + content_quoted + content_quoted
faq = Suppress('faq') + content_quoted
faq_item = content_quoted + Suppress(':') + content_quoted


cmd_mapping = {
    CommandEnum.Root: {
        CommandEnum.Service
    },
    CommandEnum.Service: {
        CommandEnum.Service,
        CommandEnum.Text,
        CommandEnum.Script,
        CommandEnum.ScriptWaiting,
        CommandEnum.FAQ
    },
    CommandEnum.FAQ: {
        CommandEnum.FAQItem
    },
    CommandEnum.Any: {
        CommandEnum.Service,
        CommandEnum.Text,
        CommandEnum.Script,
        CommandEnum.ScriptWaiting,
        CommandEnum.FAQ,
        CommandEnum.FAQItem
    }
}


"""[summary]
return value:
  (CommandEnum.Service, name, [subcommands])
"""
def identify_command(s: str) -> tuple | None:
    def safe_parse(pattern: ParserElement, s: str) -> ParseResults | None:
        try:
            result = pattern.parse_string(s, parse_all=True)
        except ParseException:
            return None
        return result

    if (r := safe_parse(service, s)) is not None:
        return (CommandEnum.Service, r[0])
    elif (r := safe_parse(text, s)) is not None:
        return (CommandEnum.Text, r[0], r[1])
    elif (r := safe_parse(script_wating, s)) is not None:
        return (CommandEnum.ScriptWaiting, r[0], r[1], r[2])
    elif (r := safe_parse(script, s)) is not None:
        return (CommandEnum.Script, r[0], r[1])
    elif (r := safe_parse(faq, s)) is not None:
        return (CommandEnum.FAQ, r[0])
    elif (r := safe_parse(faq_item, s)) is not None:
        return (CommandEnum.FAQItem, r[0], r[1])
    else:
        return None


def analyze(lines: list[str]) -> list:
    def recursive_analyze(head_type: CommandEnum, raw_struct: list[tuple[int, str] | list]) -> list[tuple] | None:
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
                print("syntax error at line %d." % line_cnt)
                fail_flag = True
                cmd_type = CommandEnum.Any
            else:
                cmd_type = command[0]
            
            if cmd_type not in cmd_mapping[head_type]:
                fail_flag = True
                print("sub-command not allowed at line %d." % line_cnt)

            sub_script = None
            if isinstance(next_elem, list):
                if cmd_type == CommandEnum.Any or cmd_type not in cmd_mapping:
                    print("no sub defination allowed under command at line %d." % line_cnt)
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
                    print("bad indentation at line %d." % line_cnt)
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
        print("analysis failed.")
        return None
    
    print("analysis succeed.")
    return script


def load_script(f: IO) -> list:
    lines = f.readlines()
    script = analyze(lines)
    
    if script is None:
        print("defination loading failed.")
        return

    print("defination loading succeeded.")
    return script

