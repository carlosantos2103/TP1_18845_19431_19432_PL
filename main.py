# Trabalho_Pratico 1 - PL 2020/21
# main.py

import ply.lex as lex
import re
from utils import readFile
from utils import writeFile
from utils import clearFile
from string import Template

testes = ["teste1.t", "teste2.t", "teste3.t", "teste4.t", "teste5.t", "teste6.t", "teste7.t", "NULL"]

tokens = ("TOTAL_TESTE", "ESTADO_TESTE", "NUMERO", "DESCRICAO", "COMENTARIO")

states = (
    ("numero", "exclusive"),
    ("descricao", "exclusive"),
)


def t_TOTAL_TESTE(t):  # 1..41
    r"""[0-9 ]+..[0-9]+"""
    return t


def t_COMENTARIO(t):  # # Comentario
    r"""[ ]*[# ][a-zA-Z0-9:'.() ]+\n"""  # TODO: adicionar? ([ ]*[# ][a-zA-Z0-9:'. ]+\n)* - para ler tudo no mesmo token (teste4)
    t.value = t.value.replace("\n", "<br>")
    return t


def t_ESTADO_TESTE(t):  # ok/not ok
    r"""[not ]*ok"""
    t.lexer.begin("numero")
    return t


def t_numero_NUMERO(t):  # 1/2/3
    r"""[0-9]+"""
    t.value = int(t.value)
    t.lexer.begin("descricao")
    return t


def t_descricao_ESTADO_TESTE(t):
    r"""[ -]*[not ]*ok[ ]"""
    t.value = t.value[:-1]
    t.value = t.value.replace(" - ", "")
    t.lexer.begin("numero")
    return t


def t_descricao_DESCRICAO(t):  # - correu bem
    r"""[ -]*([a-zA-Z0-9: ]*\n)+|[ -]+"""
    t.lexer.begin("INITIAL")
    t.value = t.value.replace("\n", "<br>")
    t.value = t.value.replace(" - ", "")
    if not t.value or t.value == " ":
        pass
    else:
        return t


def t_error(t):
    print("ERROR: \n" + t.value)
    exit(1)


def t_descricao_error(t):
    print("ERROR descricao: \n" + t.value)
    exit(1)


def t_numero_error(t):
    print("ERROR numero: \n" + t.value)
    exit(1)


t_ignore = "\n"
t_numero_ignore = " "
t_descricao_ignore = ""

nome_ficheiro = "testes/teste3.t"
lexer = lex.lex()

i=0

while testes[i] != "NULL":
    if testes[i]== "NULL":
        exit(0)
    html_file = testes[i][:-1] + "html"
    clearFile(html_file)
    writeFile(html_file, "<!DOCTYPE html>\n<html>\n<head>\n<title>TAP</title>\n</head>\n<body>\n<h1>TAP (Test Anything "
                     "Protocol)</h1>\n<h2>Ficheiro: " + testes[i] + "</h2>\n")
    lexer.input(readFile(nome_ficheiro))
    print(f"\n############ {testes[i]} ############\n")
    for token in iter(lexer.token, None):
        writeFile(html_file, """<span style="margin-left:""" + str(str(token.value).count('    ') * 2) + """em">""" + str(token.value) + " </span>")
        print(token)
        if token.type == "TOTAL_TESTE":
            writeFile(html_file, "</br>")
    if i == 0:
        writeFile(html_file, f"""<br> </br><a href= testes/"""+ testes[i + 1] + """> """ + testes[i + 1] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 2] + """> """ + testes[i + 2] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 3] + """> """ + testes[i + 3] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 4] + """> """ + testes[i + 4] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 5] + """> """ + testes[i + 5] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 6] + """> """ + testes[i + 6] + """</a>\n""")
    if i == 1:
        writeFile(html_file, f"""<br> </br><a href= testes/""" + testes[i - 1] + """> """ + testes[i - 1] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 1] + """> """ + testes[i + 1] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 2] + """> """ + testes[i + 2] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 3] + """> """ + testes[i + 3] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 4] + """> """ + testes[i + 4] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 5] + """> """ + testes[i + 5] + """</a>\n""")
    if i == 2:
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 2] + """> """ + testes[i - 2] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 1] + """> """ + testes[i - 1] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 1] + """> """ + testes[i + 1] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 2] + """> """ + testes[i + 2] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 3] + """> """ + testes[i + 3] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 4] + """> """ + testes[i + 4] + """</a>\n""")
    if i == 3:
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 3] + """> """ + testes[i - 3] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 2] + """> """ + testes[i - 2] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 1] + """> """ + testes[i - 1] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 1] + """> """ + testes[i + 1] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 2] + """> """ + testes[i + 2] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 3] + """> """ + testes[i + 3] + """</a>\n""")
    if i == 5:
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 5] + """> """ + testes[i - 5] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 4] + """> """ + testes[i - 4] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 3] + """> """ + testes[i - 3] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 2] + """> """ + testes[i - 2] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 1] + """> """ + testes[i - 1] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i + 1] + """> """ + testes[i + 1] + """</a>\n""")
    if i == 6:
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 6] + """> """ + testes[i - 6] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 5] + """> """ + testes[i - 5] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 4] + """> """ + testes[i - 4] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 3] + """> """ + testes[i - 3] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 2] + """> """ + testes[i - 2] + """</a>\n""")
        writeFile(html_file,f"""<br> </br><a href= testes/""" + testes[i - 1] + """> """ + testes[i - 1] + """</a>\n""")

    writeFile(html_file, "</body>\n</html>")
    i+=1

