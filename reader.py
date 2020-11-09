import ply.lex as lex
import sys
from utils import readFile

if len(sys.argv) == 2:
    nome_ficheiro = sys.argv[1]
else:
    nome_ficheiro = ""
    print("Sem ficheiro para analisar.")
    exit(1)

tokens = ("TOTAL_TESTE", "ESTADO_TESTE", "NUMERO", "DESCRICAO", "COMENTARIO")

states = (
    ("numero", "exclusive"),
    ("descricao", "exclusive"),
)


def t_TOTAL_TESTE(t):
    r"""[0-9 ]+..[0-9]+"""
    t.value = t.value + "<br>"
    return t


def t_COMENTARIO(t):
    r"""[ ]*[# ][a-zA-Z0-9:'.() ]+\n"""  # TODO: adicionar? ([ ]*[# ][a-zA-Z0-9:'. ]+\n)* - para ler tudo no mesmo token (teste4)
    t.value = t.value.replace("\n", "<br>")
    return t


def t_ESTADO_TESTE(t):
    r"""[not ]*ok"""
    t.lexer.begin("numero")
    return t


def t_numero_NUMERO(t):
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


def t_descricao_DESCRICAO(t):
    r"""[ -]+([a-zA-Z0-9: ]*\n)+|[ -]+|\n"""
    t.lexer.begin("INITIAL")
    t.value = t.value.replace("\n", "<br>")
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
lexer.input(readFile(nome_ficheiro))