# Trabalho_Pratico 1 - PL 2020/21
# main.py
import os
import re
from utils import writeFile
from utils import clearFile
from string import Template
import reader

def level_return(lst, level):
    fail_count = 0
    success_count = 0
    level_count = 0
    for t in lst:
        if t.level == level:
            if t.result == "ok":
                success_count += 1
            else:
                fail_count += 1
            level_count += 1
    print("\t\t-----------")
    print(f"\t\t- Nivel {level} -")
    print("\t\t-----------")
    print(f"\t. O Numero de Testes Executados: {fail_count + success_count}")
    print(f"\t. O Numero de Testes Positivos: {success_count}")
    print(f"\t. O Numero de Testes Negativos: {fail_count}")
    print(f"\t. A Percentagem de Falhas: %0.2f %% \n" % (
                fail_count / (fail_count + success_count) * 100))

class Test:
    def __init__(self, result="tba", stage=0, description="tba", level=0):
        self.result = result
        self.stage = stage
        self.description = description
        self.level = level

res = ""
lvl = 0
stg = ""

if not os.path.exists('resultados'):
    os.makedirs('resultados')

for file in reader.content:

    html_file = "resultados/result_" + file[:-2] + ".html"
    test_list = []
    clearFile(html_file)
    writeFile(html_file,
              "<!DOCTYPE html>\n<html>\n<head>\n<title>TAP</title>\n</head>\n<body>\n<h1>TAP (Test Anything Protocol)</h1>\n<h2>Ficheiro: " + file + "</h2>\n")

    reader.lexer.input(reader.content[file])

    for token in iter(reader.lexer.token, None):
        writeFile(html_file, """\n\t<span style="margin-left:""" + str(str(token.value).count('    ') * 2) + """em">""" + str(token.value) + " </span>")
        if token.type == "RESULT":
            lvl = token.value.count('    ') + 1
            res = token.value[(lvl - 1) * 4:]
        if token.type == "STAGE":
            stg = token.value
        if token.type == "DESCRIPTION":
            test = Test(res, stg, token.value, lvl)
            test_list.append(test)

        # print(token)

    # Trabalhar o numero de testes executados, numero de testes com resultado positivo e percentagem de falhas;
    fail_tests = 0
    success_tests = 0

    for test in test_list:
        if test.result == "ok":
            success_tests += 1
        else:
            fail_tests += 1

    print(f"\n\n  RELATORIO DO FICHEIRO: {file}")
    print(f". O Numero Total de Testes Executados: {fail_tests + success_tests}")
    print(f". O Numero Total de Testes Positivos: {success_tests}")
    print(f". O Numero Total de Testes Negativos: {fail_tests}")
    print(f". A Percentagem Total de Falhas: %0.2f %% \n" % (
            fail_tests / (fail_tests + success_tests) * 100))


    i = 1
    max_level = 0
    for test in test_list:
        if test.level > max_level:
            max_level = test.level
    while i < max_level + 1:
        level_return(test_list, i)
        i += 1

    # for teste in lista:
    #     print(f"{teste.result}\t{teste.stage}\t{teste.description}\t{teste.level}")

    writeFile(html_file, "\n</body>\n</html>")
