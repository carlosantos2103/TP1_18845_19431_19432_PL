# Trabalho_Pratico 1 - PL 2020/21
# main.py

import re
import reader
from views import write_HTML


class Test:
    def __init__(self, result="tba", stage=0, description="tba", level=0, comment = ""):
        self.result = result
        self.stage = stage
        self.description = description
        self.level = level
        self.comment = comment

res = ""
lvl = 0
stg = ""
com = ""

for file in reader.content:
    test_list = []
    html_file = "resultados/result_" + file[:-2] + ".html"
    reader.lexer.input(reader.content[file])

    total_tests = 0
    for token in iter(reader.lexer.token, None):
        if token.type == "TOTAL_STAGES":
            captures = re.fullmatch(r"""[ ]*[0-9]+..([0-9]+)""", token.value)
            total_tests += int(captures.group(1))
        elif token.type == "RESULT":
            lvl = token.value.count('    ') + 1
            res = token.value[(lvl - 1) * 4:]
        elif token.type == "STAGE":
            stg = token.value
        elif token.type == "COMMENT":
            com = token.value.replace("#", "- ")
        elif token.type == "DESCRIPTION":
            test = Test(res, stg, token.value, lvl, com)
            res = ""
            lvl = 0
            stg = ""
            com = ""
            test_list.append(test)

    if total_tests != len(test_list):
        write_HTML(html_file, test_list, True, file)
    else:
        write_HTML(html_file, test_list, False, file)
