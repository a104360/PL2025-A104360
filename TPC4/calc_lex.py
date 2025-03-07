import sys
import ply.lex as lex

tokens = (
    'SELECT', 'VAR', 'WHERE', 'LIMIT', 'NUMBER', 'DOT', 'COLON',
    'STRING', 'LBRACE', 'RBRACE', 'UNKNOWN'
)

# Tokens rules
def t_SELECT(t):
    r'select'
    return t

def t_VAR(t):
    r'\?[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_WHERE(t):
    r'where'
    return t

def t_LIMIT(t):
    r'LIMIT'
    return t

def t_NUMBER(t):
    r'\d+'
    return t

def t_DOT(t):
    r'\.'
    return t

def t_COLON(t):
    r':'
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

def t_LBRACE(t):
    r'\{'
    return t

def t_RBRACE(t):
    r'\}'
    return t

# Ignore whitespaces
t_ignore_WS = r'\s+'

# Unknown token
def t_UNKNOWN(t):
    r'.'
    #print(f"Token desconhecido: {t.value}")
    return t

# Error function
def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Handle \n chars
def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)

def main(filename: str):
    try:
        with open(filename, "r") as file:
            text = file.read()
        
        print(text)

        lexer = lex.lex()
        lexer.input(text)

        print("\nTokens encontrados:\n")
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Uso: python3 calc_lex.py <filename>\n")
        sys.exit(1)
    
    main(sys.argv[1])
