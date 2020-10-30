# main.py

import ply.lex as lex
from utils import readFile

tokens = ("RESULT", "STAGE", "COMMENT", "ALLSTAGES")
states = (
    ("stage", "exclusive"),
    ("comment", "exclusive"),
)


def t_RESULT(t):
    r"""[a-z ]+"""  # TODO: por "\t*" antes por causa dos subtestes?
    if "o" in t.value:
        t.value = t.value[:-1]
    t.lexer.begin("stage")
    return t


def t_ALLSTAGES(t):
    r"""[0-9]+..[0-9]+"""
    return t


def t_stage_STAGE(t):
    r"""[0-9]+"""
    t.lexer.begin("comment")
    return t


def t_comment_COMMENT(t):  # TODO: Nao tenho a certeza se o comentario pode continuar na linha de baixo
    r"""[a-zA-Z0-9 ]+\n([ ]+[^#][a-zA-Z0-9 ]+\n)*|\n"""
    t.lexer.begin("INITIAL")
    return t


def t_error(t):
    print("Unknown token: [%s]" % t.value)
    pass


def t_comment_error(t):
    t_error(t)


def t_stage_error(t):
    t_error(t)


t_ignore = "\n"
t_comment_ignore = " - "
t_stage_ignore = ""

lexer = lex.lex()
lexer.input(readFile("testes/teste2.t"))

for token in iter(lexer.token, None):
    if token.type == "RESULT":
        print(token.value, end=" ")
    if token.type == "STAGE":
        print(token.value)
