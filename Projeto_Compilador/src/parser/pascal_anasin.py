import ply.yacc as yacc
from lexer.pascal_analex import tokens 


# ====== Gramática ======

start = 'Programa'

from .programa_producoes import * 
from .atribuicoes_producoes import *
from .expressoes_producoes import *
from .declaracao_producoes import *
from .arrays_producoes import *
from .funcoes_producoes import *
from .uses__producoes import *
from .corpo_producoes import *
from .ciclos_producoes import *
from .ifelse_producoes import *
from .condicoes__producoes import *

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value {p.value}")
        print(f'Line number : {p.lineno}')
    else:
        print("Syntax error at EOF")

# ====== ======

parser = yacc.yacc(debug=True)

def rec_Parser(input_string):
    print("==================COMPILAÇÃO INICIADA==================")
    result = parser.parse(input_string)

    return result
