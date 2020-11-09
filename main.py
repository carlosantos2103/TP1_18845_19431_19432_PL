# Trabalho_Pratico 1 - PL 2020/21
# main.py

import re
from utils import writeFile
from utils import clearFile
from string import Template
import reader

html_file = "resultado.html"

class Test:
    def __init__(self, resultado="tba", numero=0, description="tba", nivel=0):
        self.result = resultado
        self.stage = numero
        self.description = description
        self.level = nivel


lista = []

# clearFile(html_file)
# writeFile(html_file,
          # "<!DOCTYPE html>\n<html>\n<head>\n<title>TAP</title>\n</head>\n<body>\n<h1>TAP (Test Anything Protocol)</h1>\n<h2>Ficheiro: " + nome_ficheiro + "</h2>\n")

result = ""
level = 0
stage = ""

for token in iter(reader.lexer.token, None):
    # writeFile(html_file, """\n\t<span style="margin-left:""" + str(str(token.value).count('    ') * 2) + """em">""" + str(token.value) + " </span>")
    if token.type == "ESTADO_TESTE":
        level = token.value.count('    ') + 1
        result = token.value[(level - 1) * 4:]
    if token.type == "NUMERO":
        stage = token.value
    if token.type == "DESCRICAO":
        teste = Test(result, stage, token.value, level)
        lista.append(teste)

    # print(token)

# Trabalhar o numero de testes executados, numero de testes com
# resultado positivo e percentagem de falhas;
contador_testes_negativos = 0
contador_testes_positivos = 0

for teste in lista:
    if teste.result == "ok":
        contador_testes_positivos += 1
    else:
        contador_testes_negativos += 1

print(f"\n\n  RELATORIO DO FICHEIRO: {reader.nome_ficheiro[7:]}")
print(f". O Numero Total de Testes Executados: {contador_testes_negativos + contador_testes_positivos}")
print(f". O Numero Total de Testes Positivos: {contador_testes_positivos}")
print(f". O Numero Total de Testes Negativos: {contador_testes_negativos}")
print(f". A Percentagem Total de Falhas: %0.2f %% \n" % (
            contador_testes_negativos / (contador_testes_negativos + contador_testes_positivos) * 100))


def level_return(lista, nivel):
    contador_testes_negativos = 0
    contador_testes_positivos = 0
    contador_nivel = 0
    for teste in lista:
        if teste.level == nivel:
            if teste.result == "ok":
                contador_testes_positivos += 1
            else:
                contador_testes_negativos += 1
            contador_nivel += 1
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
while i < max_level + 1:
    level_return(lista, i)
    i += 1

# for teste in lista:
#     print(f"{teste.result}\t{teste.stage}\t{teste.description}\t{teste.level}")

# writeFile(html_file, "\n</body>\n</html>")
