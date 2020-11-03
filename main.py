# Trabalho_Pratico v1.0
import ply.lex as lex
from utils import readFile

# 1..4
# ok 1 - First test to something
# not ok 2 - Something else being tested
# ok 3 - Third test on something else
# ok 4 - Fourth test

ficheiros = ["teste3.t", "NULL"]

tokens = ("TOTAL_TESTE", "ESTADO_TESTE", "NUMERO", "COMENTARIO")

states = (
    ("numero", "exclusive"),
    ("comentario", "exclusive"),
)


def t_TOTAL_TESTE(t):  # 1..41
    r"""[0-9 ]+..[0-9]+"""
    return t


def t_ESTADO_TESTE(t):  # ok/not ok
    r"""[o|k|n| |t]+"""
    if "o" in t.value:
        t.value = t.value[:-1]
        t.lexer.begin("numero")
        return t
    pass


def t_numero_NUMERO(t):  # 1/2/3
    r"""[0-9]+"""
    t.value = int(t.value)
    t.lexer.begin("comentario")
    return t


def t_comentario_COMENTARIO(t):
    # r"""[^\n]*\n""" \n --- \n   # asdasdas
    r"""\n[ ]*[# ][a-zA-Z0-9: ]+\n|[a-zA-Z0-9: ]*\n"""
    t.lexer.begin("INITIAL")
    return t


def t_error(t):
    print("ERROR: \n" + t.value)
    exit(1)


def t_comentario_error(t):
    print("ERROR comentario: \n" + t.value)
    exit(1)


def t_numero_error(t):
    print("ERROR numero: \n" + t.value)
    exit(1)


t_ignore = "\n"
t_numero_ignore = ""
t_comentario_ignore = " - "

lexer = lex.lex()

lista = []

nome_ficheiro = ""
i = 0
while ficheiros[i] != "NULL":
    nome_ficheiro = ficheiros[i]
    lexer.input(readFile(nome_ficheiro))
    print(f"\n############ Ficheiro Nº{i + 1} ############\n")
    for token in iter(lexer.token, None):
        print(token)
    i += 1
