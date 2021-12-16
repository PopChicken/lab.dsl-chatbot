import traceback
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank_service.settings')
from django.core.management import execute_from_command_line
execute_from_command_line([sys.path[0], 'check'])


import tests.test_auth as test_auth
import tests.test_bot as test_bot
import tests.test_parser as test_parser

from typing import Callable


parser_tester = test_parser.TestParser()
bot_tester = test_bot.TestBot()
auth_tester = test_auth.TestAuth()

tot_cnt = 0
fail_cnt = 0


def safe_test(test: Callable):
    global tot_cnt, fail_cnt
    tot_cnt += 1
    try:
        test()
    except AssertionError:
        fail_cnt += 1
        print(f"test '{test.__name__}' failed.")
        traceback.print_exc()


if __name__ == '__main__':
    print("start unit test process.")
    safe_test(parser_tester.test_complicated)
    safe_test(parser_tester.test_empty)
    safe_test(parser_tester.test_incorrect)
    safe_test(parser_tester.test_naughty_indent)
    safe_test(parser_tester.test_recursive)

    safe_test(bot_tester.test_complicated)

    safe_test(auth_tester.test_expire)
    safe_test(auth_tester.test_generate)
    safe_test(auth_tester.test_preprocess)

    print(f"test completed. ({tot_cnt - fail_cnt}/{tot_cnt} succeed)")
    
    exit(0)
