# ====== Produções da zona de uses/imports ======


def p_duses(p):
    '''
    Duses : USES UseList ';'
          | 
    '''

def p_uselist(p):
    '''
    UseList : UseList ',' ID
            | ID 
    '''