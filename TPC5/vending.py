import sys
import ply.lex as lex
import re

stock = dict()

credit = 0

def displayItems():
    print("maq:\n")
    print("cod\t|  nome\t|  quantidade\t|  preço\n")


def selectItem(item):
    print(f'CREDIT : {credit}')

def coin(coin : str):
    global credit
    if coin.endswith('e'):
        credit += int(coin.strip('ec'))
    else:
        credit += float(coin.strip('ec')) / 100

states = (
    ('CHARGE','exclusive'),
    ('SELECT','exclusive')
)

tokens = (
    'MOEDA',
    'COD',
    'LIST'
)

# Definition of the 
def t_CHARGE_MOEDA(t):
    r'\d+[ec]'
    coin(t.value)
    return t

def t_CHARGE_newline(t):
    r'\n+'
    t.lexer.begin("INITIAL")

def t_SELECT_COD(t):
    r'[A-Z]\d{1,2}'
    # Call select function
    selectItem(t.value)
    t.lexer.begin('INITIAL')
    return t

def t_SELECT(t):
    r'SELECT'
    t.lexer.begin("SELECT")

def t_LIST(t):
    r'LISTAR'
    displayItems()
    return t

def t_MOEDA(t):
    r'MOEDA'
    t.lexer.begin("CHARGE")
    return t
    

def t_ANY_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

t_ignore = ' \t,\n'
t_CHARGE_ignore = ' \t,'
t_SELECT_ignore = ' \t'



def getStock() -> dict:
    text = ""
    with open("stock.json","r") as file:
        text = file.read()
    
    matches = re.findall(r'"cod":[ ]*(\"\w+\"),\n*[ ]*\"nome\":[ ]*(\"(?:.*?)\"),\n?[ ]*"quant":[ ]*(\d+),\n?[ ]*"preco":[ ]*(\d+.\d*)',text)

    for a in matches:
        stock[a[0]] = [a[1],int(a[2]),float(a[3])]

    return stock


def main():
    """
    Commands:
        - LISTAR
        - MOEDA [1e,20c,5c]
        - SELECIONAR A23 (exist / dont exist)
        - SAIR
    """
    
    # Load items 
    stock = getStock()

    credit = 0

    # Cycle to read command

    lexer = lex.lex()

    for a in sys.stdin:
        lexer.input(a)
        for tok in lexer:
            print(tok)
        #match = re.findall(r'LISTAR\n?|MOEDA (\d+[ec],?[ ]*)*|SELECIONAR[ ]*\w+|SAIR',a,re.IGNORECASE)


    # Update items & shutdown


if __name__ == "__main__":
    main()