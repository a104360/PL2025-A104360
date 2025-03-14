import ply.lex as lex

# Define states
states = (
    ('COMMENT', 'exclusive'),
    ('STRING', 'exclusive'),
)

# List of token names
tokens = [
    'NUMBER',
    'WORD',
    'COMMENT_TEXT',
    'STRING_TEXT'
]

# Regular expressions for tokens in the default state
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_WORD(t):
    r'[a-zA-Z]+'
    return t

# Comment state rules
def t_COMMENT_start(t):
    r'/\*'
    t.lexer.begin('COMMENT')

def t_COMMENT_TEXT(t):
    r'[^*]+'
    pass  # Ignore comment content

def t_COMMENT_end(t):
    r'\*/'
    t.lexer.begin('INITIAL')

# String state rules
def t_STRING_start(t):
    r'"'
    t.lexer.begin('STRING')

def t_STRING_TEXT(t):
    r'[^"]+'
    return t

def t_STRING_end(t):
    r'"'
    t.lexer.begin('INITIAL')

# Ignored characters
t_ignore = ' \t'
t_COMMENT_ignore = ''
t_STRING_ignore = ''

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test the lexer
data = '''
hello 123 "this is a string" /* this is a comment */
'''

lexer.input(data)

for tok in lexer:
    print(tok)
