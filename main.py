# Trabalho_Pratico 1 - PL 2020/21
# main.py

import os
import re
import reader
from utils import writeFile
from utils import clearFile

def addScript():
    script = "\n<script>"
    for j in range(1, len(test_list)+1):
        script = script + """\nfunction viewDesc""" + str(j) + """() {document.getElementById('desc""" + str(j) + """').style.display = "inline";}\nfunction closeDesc""" + str(j) + """() {document.getElementById('desc""" + str(j) + """').style.display = "none";}"""
        j+=1
    return script + "</script>"

def addSumm():
    fail_tests = 0
    success_tests = 0
    for tst in test_list:
        if tst.result == "ok":
            success_tests += 1
        else:
            fail_tests += 1

    percent_fail = round(fail_tests/(fail_tests+success_tests)*100, 2)
    percent_success = round(success_tests / (fail_tests + success_tests) * 100, 2)

    writeFile(html_file,
              """\n<div class="results">\n- Total de testes: """ + str(fail_tests + success_tests) + "<br>"
              """\n- Testes com sucesso: <span style=color:green>""" + str(success_tests) + """ ("""+ str(percent_success) +""" %)<br></span>"""
              """\n- Testes com falhas: <span style=color:red>""" + str(fail_tests) + """  ("""+ str(percent_fail) +""" %)<br></span>\n</div>""")
    pass


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

if not os.path.exists('resultados'):
    os.makedirs('resultados')

for file in reader.content:

    html_file = "resultados/result_" + file[:-2] + ".html"
    test_list = []
    clearFile(html_file)
    writeFile(html_file,
            """<!DOCTYPE html>\n<html>\n<head>\n<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
            <link href="../style.css" rel="stylesheet" type="text/css">
            <title>Test Anything Protocol</title>
            </head>\n<body>\n<h1 class="title">Resultados TAP</h1>\n<h2 class="title2">Test Anything Protocol</h2>\n<h2 class="file" >Ficheiro: """ + file + """</h2>\n<div class="container">\n<div id="menu" class="menu">""")
    i=1
    for f in reader.content:
        writeFile(html_file,

            "\n<button style=width:" + str(100/len(reader.content))+ """% type="button" onclick="window.location.href='result_""" + f[:-2] + """.html';">Ficheiro""" + str(i) + "</button>")
        i+=1

    writeFile(html_file, "</div>")
    reader.lexer.input(reader.content[file])

    total_tests = 0
    for token in iter(reader.lexer.token, None):
        if token.type == "TOTAL_STAGES":
            captures = re.fullmatch(r"""[ ]*[0-9]+..([0-9])+""", token.value)
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
        writeFile(html_file, """\n<div>\n<span style=color:red;font-size:large;margin:2em;><i>Não foi possível apresentar resutlados para este ficheiro.</i></span>\n</div>\n</body>\n</html>""")
        continue

    addSumm()

    i = 1
    for test in test_list:
        if test.comment != "":
            if "TODO" in test.comment:
                writeFile(html_file, """\n<div class="com">\n<span style=color:#cccc00><i>""" + test.comment + "</i></span>\n</div>\n")
            else:
                writeFile(html_file, """\n<div class="com">\n<span style=color:#737373><i>""" + test.comment + "</i></span>\n</div>\n")
        writeFile(html_file, """\n\t<span class="test" onmouseenter="viewDesc""" + str(i) + """()" onmouseout="closeDesc""" + str(i) + """()" style=margin-left:""" + str((test.level - 1) * 2) + """em;""")
        if test.result == "ok":
            writeFile(html_file, """color:green>""")
        else:
            writeFile(html_file, """color:red>""")
        writeFile(html_file, str(test.stage) + "  |  " + test.result + """ </span><span id="desc""" + str(i) + """" style=color:#949494;margin-left:1em;display:none><i>""" + test.description + "</i></span><br>")
        i+=1

    writeFile(html_file, "\n</div>\n" + addScript() + "\n</body>\n</html>")

























clearFile("resultado.html")
writeFile("resultado.html",
            """<!DOCTYPE html>\n<html>\n<head>\n<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
            <link href="style.css" rel="stylesheet" type="text/css">
            <title>Test Anything Protocol</title>
            </head>\n<body>\n<h1 class="title">Resultados TAP</h1>\n<h2 class="title2">Test Anything Protocol</h2>\n<div class="container">\n<div id="menu" class="menu">""")

i=1
for f in reader.content:
    writeFile("resultado.html",
              "\n<button style=width:" + str(100/len(reader.content)) + """% type="button2" class="button2" onclick="window.location.href='resultados/result_""" + f[:-2] + """.html';">Ficheiro""" + str(i) + "</button>")
    i += 1

writeFile("resultado.html", "\n</div>\n</div>\n</body>\n</html>")



