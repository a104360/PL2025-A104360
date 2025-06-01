# ====== Produções do corpo do programa ======

def p_localinstslist_multiple(p):
    '''
    LocalInstsList : LocalInstsList ';' Instrucao
    '''
    p[0] = p[1] + "\n" + p[3]

def p_localinstslist_terminada(p):
    '''
    LocalInstsList : LocalInstsList ';'
    '''
    p[0] = p[1]

def p_localinstslist_single(p):
    '''
    LocalInstsList : Instrucao 
    '''
    p[0] = p[1]


def p_instrucao(p):
    '''
    Instrucao : While
              | CicloFor
              | InstrucaoCondicional
              | Atribuicao 
              | Expressao
    '''
    p[0] = p[1]
    print("Acabei de ler um instrucao")


def p_instrucao_bloco(p):
     '''
     Instrucao : Bloco
     '''
     p[0] = p[1]


def p_bloco(p):
    '''
    Bloco : BEGIN LocalInstsList END 
    '''
    p[0] = p[2]

