# Trabalho_Pratico 1 - PL 2020/21
# main.py
import os
import re
from utils import writeFile
from utils import clearFile
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

def addScript():
    script = "\n<script>"
    for j in range(1, len(test_list)+1):
        script = script + """\nfunction viewDesc""" + str(j) + """() {document.getElementById('desc""" + str(j) + """').style.display = "inline";}\nfunction closeDesc""" + str(j) + """() {document.getElementById('desc""" + str(j) + """').style.display = "none";}"""
        j+=1
    return script + "</script>"

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
            """<!DOCTYPE html>\n<html>\n<head>\n<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
            <link href="../style.css" rel="stylesheet" type="text/css">
            <script src="../result.js"></script>
            <title>Test Anything Protocol</title>
            </head>\n<body>\n<h1 class="title">Resultados TAP</h1>\n<h2 class="title2">Test Anything Protocol</h2>\n<h2 class="file" >Ficheiro: """ + file + """</h2>\n<div class="container">\n<div id="menu" class="menu">""")
    i=1
    for f in reader.content:
        writeFile(html_file,
            "\n<button style=width:" + str(98/len(reader.content))+ """% type="button" onclick="window.location.href='result_""" + f[:-2] + """.html';">Ficheiro""" + str(i) + "</button>")
        i+=1

    writeFile(html_file, "</div>")
    reader.lexer.input(reader.content[file])

    for token in iter(reader.lexer.token, None):
        if token.type == "RESULT":
            lvl = token.value.count('    ') + 1
            res = token.value[(lvl - 1) * 4:]
        if token.type == "STAGE":
            stg = token.value
        if token.type == "DESCRIPTION":
            test = Test(res, stg, token.value, lvl)
            test_list.append(test)

    fail_tests = 0
    success_tests = 0

    for test in test_list:
        if test.result == "ok":
            success_tests += 1
        else:
            fail_tests += 1

    percent_fail = round(fail_tests/(fail_tests+success_tests)*100, 2)
    percent_success = round(success_tests / (fail_tests + success_tests) * 100, 2)

    writeFile(html_file,
              """\n\t<span class="results">- Total testes: """ + str(fail_tests + success_tests) + "<br></span>"
              """<span class="results">- Teste com sucesso: </span><span class="results" style=color:green>""" + str(success_tests) + """ ("""+ str(percent_success) +""" %)<br></span>"""
              """<span class="results">- Testes com falhas: </span><span class="results"style=color:red>""" + str(fail_tests) + """  ("""+ str(percent_fail) +""" %)<br></span>""")

    i = 1
    for test in test_list:
        writeFile(html_file, """\n\t<span class="test" onmouseenter="viewDesc""" + str(i) + """()" onmouseout="closeDesc""" + str(i) + """()" style=margin-left:""" + str((test.level - 1) * 2) + """em;""")
        if test.result == "ok":
            writeFile(html_file, """color:green>""")
        else:
            writeFile(html_file, """color:red>""")
        writeFile(html_file, str(test.stage) + "  |  " + test.result + """ </span><span id="desc""" + str(i) + """" style=color:#949494;margin-left:1em;display:none><i>""" + test.description + "</i></span><br>")
        i+=1

    writeFile(html_file, "\n</div>\n" + addScript() + "\n</body>\n</html>")
