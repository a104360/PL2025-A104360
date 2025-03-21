import sys
import ply.lex as lex
import re
from datetime import datetime

stock = dict()

credit = {
    "2e":0,
    "1e":0,
    "50c":0,
    "20c":0,
    "10c":0,
    "5c":0,
    "2c":0
}

machineID = ""


def getCredit():
    global credit
    sum = 0
    for a in credit:
        if a.endswith('e'):
            sum += int(a.strip('ec')) * credit[a]
        else:
            sum += (float(a.strip('ec')) / 100) * credit[a]
    return sum

def getCents() -> tuple[int,int]:
    global credit
    sum = 0
    sum += credit['50c'] * 50
    sum += credit['20c'] * 20
    sum += credit['10c'] * 10
    sum += credit['5c'] * 5
    sum += credit['2c'] * 2
    offset = 0
    while sum > 100:
        offset += 1
        sum -= 100
    return (offset,sum)

def getEuros():
    global credit
    offset_cents = getCents()
    sum = 0
    sum += credit['1e']
    sum += credit['2e'] * 2
    return str(sum+offset_cents[0]) + 'e' + str(offset_cents[1]) + 'c'
    

def selectItem(code):
    global credit, stock
    if code not in stock:
        print(f'{machineID}: Código inválido')
        print(f'{machineID}: Saldo = {getEuros()}')
        return
        
    item = stock[code]
    # Check if item is in stock
    if item[1] > 0:  
        current_credit = getCredit()
        # Check if enough credit
        if current_credit >= item[2]:  
        
            # Item is available and affordable
            remaining_credit = current_credit - item[2]
            
            # Reset credit dictionary
            for coin_type in credit:
                credit[coin_type] = 0
                
            # Convert remaining amount back to coins (starting with largest)
            remaining_euros = int(remaining_credit)
            remaining_cents = round((remaining_credit - remaining_euros) * 100)
            
            # Add euros back to credit
            while remaining_euros >= 2:
                credit['2e'] += 1
                remaining_euros -= 2
            
            if remaining_euros == 1:
                credit['1e'] += 1
            
            # Add cents back to credit
            while remaining_cents >= 50:
                credit['50c'] += 1
                remaining_cents -= 50
            
            while remaining_cents >= 20:
                credit['20c'] += 1
                remaining_cents -= 20
            
            while remaining_cents >= 10:
                credit['10c'] += 1
                remaining_cents -= 10
            
            while remaining_cents >= 5:
                credit['5c'] += 1
                remaining_cents -= 5
            
            while remaining_cents >= 2:
                credit['2c'] += 1
                remaining_cents -= 2
            
            # Adjust inventory
            item[1] -= 1
            print(f'{machineID}: Pode retirar o produto dispensado {item[0]}')
            print(f'{machineID}: Saldo = {getEuros()}')
        else:
            print(f'{machineID}: Crédito insuficiente')
            print(f'{machineID}: Saldo = {getEuros()}')
    else:
        print(f'{machineID}: Produto indisponível')
        print(f'{machineID}: Saldo = {getEuros()}')

        
def displayItems():
    print("maq:\n")
    print("cod\t|\tnome\t|\tquantidade\t|\tpreço\n------------------------")
    for a in stock:
        print(f'{a}\t{stock[a][0]}\t\t{stock[a][1]}\t\t{stock[a][2]}')


def getChange():
    global credit
    text = ""
    for a in credit:
        if a != '2c':
            if credit[a] > 0:text += f"{credit[a]}x {a}, "
            continue
        if credit[a] > 0:text += f'{credit[a]}x {a}.'
    return text

def coin(coin : str):
    global credit
    credit[coin] += 1
    getCredit()

states = (
    ('CHARGE','exclusive'),
    ('SELECT','exclusive')
)

tokens = (
    'MOEDA',
    'COD',
    'LIST',
    'EXIT'
)

def t_EXIT(t):
    r'SAIR'
    print(f"{machineID}: Pode retirar o troco:{getChange()}")
    print(f"{machineID}: Até à próxima")
    exit(0)

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
    #return t

def t_SELECT(t):
    r'SELECIONAR'
    t.lexer.begin("SELECT")

def t_LIST(t):
    r'LISTAR'
    displayItems()
    #return t

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



def loadMachine() -> dict:
    """Loads the machine with id and stock"""
    text = ""
    with open("stock.json","r") as file:
        text = file.read()

    # Load machine id
    global machineID 
    machineID = re.findall(r'"maq":\"(\w+)\"',text)[0]
    print(f'{machineID}: {datetime.today().date()}')
    

    # Load Stock
    matches = re.findall(r'"cod":[ ]*\"(\w+)\",\n*[ ]*\"nome\":[ ]*\"((?:.*?))\",\n?[ ]*"quant":[ ]*(\d+),\n?[ ]*"preco":[ ]*(\d+.\d*)',text)

    for a in matches:
        stock[a[0]] = [a[1],int(a[2]),float(a[3])]

    print(f'Stock carregado, ')
    return stock


def main():
    """
    Commands:
        - LISTAR
        - MOEDA [1e,20c,5c]
        - SELECIONAR A23 (exist / dont exist)
        - SAIR
    """
    global stock,credit
    
    # Load items 
    stock = loadMachine()
    print('Estado atualizado.')

    print(f'{machineID}: Bom dia. Estou disponível para atender o seu pedido.')

    # Cycle to read command

    lexer = lex.lex()

    sys.stdout.write('>>')
    sys.stdout.flush()


    for a in sys.stdin:
        lexer.input(a)
        for tok in lexer:
            print(tok)
        sys.stdout.write('>>')
        sys.stdout.flush()
        #match = re.findall(r'LISTAR\n?|MOEDA (\d+[ec],?[ ]*)*|SELECIONAR[ ]*\w+|SAIR',a,re.IGNORECASE)


    # Update items & shutdown


if __name__ == "__main__":
    main()