
import sys
from analex import lexer
from Exp_ast import Exp, Num

prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro sintático, token inesperado: ", simb)

def rec_term(simb):
    global prox_simb
    if prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        parserError(prox_simb)
        prox_simb = ('erro', '', 0, 0)

def rec_Exp():
    global prox_simb
    if prox_simb.type == 'NUM':
        print("Derivando por P1: Exp    --> num ExpCont")
        num = prox_simb.value
        exp1 = Num('num',num)
        rec_term('NUM')
        op, exp2 = rec_ExpCont()
        if(op and exp2):
            print("Reconheci P1: Exp    --> num ExpCont")
            return Exp('exp', exp1, op, exp2)
        else: 
            print("Reconheci P1: Exp    --> num ExpCont")
            return exp1
    else:
        parserError(prox_simb)

def rec_ExpCont():
    global prox_simb
    if not prox_simb:
        print("Derivando por P2: ExpCont -->    ")
        print("Reconheci P2: ExpCont -->    ")
        return None, None
    elif prox_simb.type == 'OP':
        print("Derivando por P3: ExpCont --> Op Exp")
        op = prox_simb.value
        rec_term('OP')
        res = rec_Exp()
        print("Reconheci P3: ExpCont --> Op Exp")
        return op, res
    else:
        parserError(prox_simb)

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    res = rec_Exp()
    res.pp()
    print("\n")
    print(res.value())
    return res
    


if __name__ == '__main__':
    for line in sys.stdin:
        rec_Parser(line)