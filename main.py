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
    t.value = t.value + "<br>"
    return t


def t_COMENTARIO(t):  # # Comentario
    r"""[ ]*[# ][a-zA-Z0-9:'.() ]+\n"""
    # TODO: adicionar? ([ ]*[# ][a-zA-Z0-9:'. ]+\n)* - para ler tudo no mesmo token (teste4)
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
    r"""[ -]+([a-zA-Z0-9: ]*\n)+|[ -]+|\n"""
    t.lexer.begin("INITIAL")
    t.value = t.value.replace("\n", "")
    t.value = t.value.replace(" - ", "")
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


class Test:
    def __init__(self, resultado="tba", numero=0, description="tba", nivel=0):
        self.result = resultado
        self.stage = numero
        self.description = description
        self.level = nivel


lista = []

t_ignore = "\n"
t_numero_ignore = " "
t_descricao_ignore = ""

html_file = "teste.html"
nome_ficheiro = "testes/teste3.t"
clearFile(html_file)
writeFile(html_file, "<!DOCTYPE html>\n<html>\n<head>\n<title>TAP</title>\n</head>\n<body>\n<h1>TAP (Test Anythin"
                     "g Protocol)</h1>\n<h2>Ficheiro: " + nome_ficheiro + "</h2>\n")
lexer = lex.lex()
lexer.input(readFile(nome_ficheiro))

result = ""
level = 0
stage = ""

for token in iter(lexer.token, None):
    #     writeFile(html_file,
    #               """\n\t<span style="margin-left:""" + str(str(token.value).count('    ') * 2) + """em">""" + str(
    #                   token.value) + " </span>")
    if token.type == "ESTADO_TESTE":
        level = token.value.count('    ') + 1
        if level == 1:
            result = token.value
            print(result)
        else:
            result = token.value[(level-1)*4:]
            print(result)
    if token.type == "NUMERO":
        stage = token.value
    if token.type == "DESCRICAO":
        teste = Test(result, stage, token.value, level)
        lista.append(teste)

    #print(token)


# Trabalhar o numero de testes executados, numero de testes com
# resultado positivo e percentagem de falhas;
contador_testes_negativos = 0
contador_testes_positivos = 0

for teste in lista:
    if teste.result == "ok":
        contador_testes_positivos+=1
    else:
        contador_testes_negativos+=1


print(f"\n\n  RELATORIO DO FICHEIRO: {nome_ficheiro[7:]}")
print(f". O Numero Total de Testes Executados: {contador_testes_negativos+contador_testes_positivos}")
print(f". O Numero Total de Testes Positivos: {contador_testes_positivos}")
print(f". O Numero Total de Testes Negativos: {contador_testes_negativos}")
print(f". A Percentagem Total de Falhas: %0.2f %% \n" % (contador_testes_negativos/(contador_testes_negativos+contador_testes_positivos) * 100))


def level_return(lista, nivel):
    contador_testes_negativos = 0
    contador_testes_positivos = 0
    contador_nivel = 0
    for teste in lista:
        if teste.level == nivel:
            if teste.result == "ok":
                contador_testes_positivos+=1
            else:
                contador_testes_negativos+=1
            contador_nivel+=1
    print("\t\t-----------")
    print(f"\t\t- Nivel {nivel} -")
    print("\t\t-----------")
    print(f"\t. O Numero de Testes Executados: {contador_testes_negativos + contador_testes_positivos}")
    print(f"\t. O Numero de Testes Positivos: {contador_testes_positivos}")
    print(f"\t. O Numero de Testes Negativos: {contador_testes_negativos}")
    print(f"\t. A Percentagem de Falhas: %0.2f %% \n" % (
                contador_testes_negativos / (contador_testes_negativos + contador_testes_positivos) * 100))

i = 1
max_level = 0
for teste in lista:
    if teste.level > max_level:
        max_level = teste.level
while i < max_level+1:
    level_return(lista, i)
    i+=1

#for teste in lista:
#    print(f"{teste.result}\t{teste.stage}\t{teste.description}\t{teste.level}")

writeFile(html_file, "\n</body>\n</html>")

# i = 0

# while testes[i] != "NULL":
#     if testes[i] == "NULL":
#         exit(0)
#     html_file = testes[i][:-1] + "html"
#     clearFile(html_file)
#     writeFile(html_file, "<!DOCTYPE html>\n<html>\n<head>\n<title>TAP</title>\n</head>\n<body>\n<h1>TAP (Test Anythin"
#                          "g Protocol)</h1>\n<h2>Ficheiro: " + testes[i] + "</h2>\n")
#     lexer.input(readFile("testes/" + testes[i]))
#     print(f"\n############ {testes[i]} ############\n")
#     for token in iter(lexer.token, None):
#         writeFile(html_file,
#                   """\n\t<span style="margin-left:""" + str(str(token.value).count('    ') * 2) + """em">""" + str(
#                       token.value) + " </span>")
#         print(token)
#     for j in range(7):
#         writeFile(html_file,
#                   f"""\n<br> </br><a href= """ + html_file + """> """ + testes[j] + """</a>""")
#     writeFile(html_file, "\n</body>\n</html>")
#     i += 1
