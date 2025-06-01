# ====== Produções Principais ======


def p_programa(p):
    '''
    Programa : PROGRAM ID ';' Duses GlobalInsts BlocoPrincipal '.'
    '''

    lvars = ""
    lfuncs = ""

    for type,code in p[5]:
        if type == "vars":
            lvars += code
        else:
            lfuncs += code


    p[0] = lvars +  "\nSTART\n" + p[6] + "\nSTOP" + lfuncs


def p_globalinsts(p):
    '''
    GlobalInsts : GlobalInsts GlobalInst
                | 
    '''
    if len(p) == 3:

        p[0] = p[1] + p[2]
    else:
        p[0] = []

def p_globalinst_func(p):
    '''
    GlobalInst : Dfuncao
               | Dprocedimento
    '''
    p[0] = [("func",p[1])]

def p_globalinst_var(p):
    '''
    GlobalInst : Dvariaveis
    '''

    p[0] = [("vars",p[1])]
    print("Acabei de ler uma instrução global")


def p_blocofinal(p):
    '''
    BlocoPrincipal : BEGIN LocalInstsList END
    '''

    p[0] = p[2]
