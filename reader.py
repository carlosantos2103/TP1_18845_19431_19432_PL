import ply.lex as lex
import sys
import os
from utils import readFile

content = {}
if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
    content[os.path.basename(sys.argv[1])] = (readFile(sys.argv[1]))
elif len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
    for file in os.listdir(sys.argv[1]):
        content[file]=(readFile(sys.argv[1]+"/"+file))
else:
    print("Sem ficheiro(s) para analisar.")
    exit(1)

tokens = ("TOTAL_STAGES", "RESULT", "STAGE", "DESCRIPTION", "COMMENT")

states = (
    ("stage", "exclusive"),
    ("description", "exclusive"),
)


def t_TOTAL_STAGES(t):
    r"""[0-9 ]+..[0-9]+"""
    return t


def t_COMMENT(t):
    r"""[ ]*\#[ ][^\n]+\n([ ]*\#[ ][^\n]+\n)*"""
    return t


def t_RESULT(t):
    r"""[not ]*ok"""
    t.lexer.begin("stage")
    return t


def t_stage_STAGE(t):
    r"""[0-9]+"""
    t.value = int(t.value)
    t.lexer.begin("description")
    return t


def t_description_DESCRIPTION(t):
    r"""[ -]+([a-zA-Z0-9: ]*\n)+|[ -]+|\n"""
    t.lexer.begin("INITIAL")
    t.value = t.value.replace("\n", "")
    t.value = t.value.replace(" - ", "")
    return t


def t_error(t):
    print("ERRO no reconhecimento do conteúdo do ficheiro.")
    exit(1)


def t_description_error(t):
    print("ERRO no reconhecimento do conteúdo do ficheiro.")
    exit(1)


def t_stage_error(t):
    print("ERRO no reconhecimento do conteúdo do ficheiro.")
    exit(1)


t_ignore = "\n"
t_stage_ignore = " "
t_description_ignore = ""

lexer = lex.lex()