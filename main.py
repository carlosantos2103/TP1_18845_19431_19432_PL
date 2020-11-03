# Trabalho_Pratico 1 - PL 2020/21
# main.py

import ply.lex as lex
import re
from utils import readFile

# 1..4
# ok 1 - First test to something
# not ok 2 - Something else being tested
# ok 3 - Third test on something else
# ok 4 - Fourth test

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
    t.value = t.value.replace("\n", "")
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
    r"""[not ]*ok"""
    return t


def t_descricao_NUMERO(t):
    r"""[0-9]+"""
    t.value = int(t.value)
    t.lexer.begin("INITIAL")
    return t


def t_descricao_DESCRICAO(t):  # - correu bem
    r"""[ -]*([a-zA-Z0-9: ]*\n)+|[ -]+"""
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


t_ignore = "\n"
t_numero_ignore = " "
t_descricao_ignore = ""

lexer = lex.lex()

nome_ficheiro = "testes/teste6.t"
lexer.input(readFile(nome_ficheiro))
print(f"\n############ {nome_ficheiro} ############\n")
for token in iter(lexer.token, None):
    if token.type == "TOTAL_TESTE":
        captures = re.fullmatch(r"""([ ]*)[0-9]+..([0-9]+)""", token.value)
        print(f"{captures.group(1)}Total testes: {captures.group(2)}")

    print(token)
