import ply.lex as lex

tokens = ('NUM', 'OP')

t_NUM = r'\d+'
t_OP = r'(\+|\-|\*)'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = '\t '

def t_error(t):
    print('Carácter desconhecido: ', t.value[0], 'Linha: ', t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()