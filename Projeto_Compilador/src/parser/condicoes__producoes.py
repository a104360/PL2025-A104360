# ====== Produções de Condições ======

def p_Condicao(p):
    '''
    Condicao : Condicao AND Condicao
             | Condicao OR Condicao
             | NOT Condicao
             | DeclaracaoCondicao
             | '(' Condicao ')'
    '''
    if len(p) == 4:
        if p[2].upper() in ("AND", "OR"):
            left = p[1]
            right = p[3]
            logic_op = p[2].upper()
            op_code = "AND" if logic_op == "AND" else "OR"
            p[0] = f"{left}\n{right}\n{op_code}"
        else:
            p[0] = p[2]

    elif len(p) == 3:
        inner = p[2]
        p[0] = f"{inner}\nNOT"
    else:
        p[0] = p[1]

def p_DeclaracaoCondicao(p):
    '''
    DeclaracaoCondicao : Expressao SimboloCondicional Expressao
                       | Expressao
    '''
    if len(p) == 4:

        left_val, left_type, left_code = p[1]
        right_val, right_type, right_code = p[3]
        op_code = p[2]

        if left_type != right_type:
            print("Erro: tipos incompatíveis na condição")
            p[0] = "; erro de tipo"
            return

        # Constant folding
        if left_code == "" and right_code == "":
            result = eval_condition(op_code, left_val, right_val)
            p[0] = f"PUSHI {1 if result else 0}"
        else:
            if left_code:
                left_push = left_code
            else:
                if left_type == "integer":
                    left_push = f"PUSHI {left_val}"
                elif left_type == "real":
                    left_push = f"PUSHF {left_val}"
                elif left_type == "string":
                    limpo = left_val.strip("'")
                    left_push = f'PUSHS "{limpo}"\nCHRCODE'
                else:
                    print(f"Erro: tipo desconhecido '{left_type}' no lado esquerdo")
                    p[0] = "; erro de tipo"
                    return

            if right_code:
                right_push = right_code
            else:
                if right_type == "integer":
                    right_push = f"PUSHI {right_val}"
                elif right_type == "real":
                    right_push = f"PUSHF {right_val}"
                elif right_type == "string":
                    limpo = right_val.strip("'")
                    right_push = f'PUSHS "{limpo}"\nCHRCODE'
                else:
                    print(f"Erro: tipo desconhecido '{right_type}' no lado direito")
                    p[0] = "; erro de tipo"
                    return

            
            p[0] = f"{left_push}\n{right_push}\n{op_code}"

    else:
        val, val_type, val_code = p[1]
        if val_type != "boolean":
            print("Erro: condição esperava valor booleano")
        if val_code:
            p[0] = val_code
        else:
            p[0] = f"PUSHI {1 if val else 0}"




def eval_condition(op, left, right):
    if op == "EQUAL":
        return left == right
    elif op == "NEQ":
        return left != right
    elif op == "INF":
        return left < right
    elif op == "INFEQ":
        return left <= right
    elif op == "SUP":
        return left > right
    elif op == "SUPEQ":
        return left >= right
    return False



def p_SimboloCondicional(p):
    '''
    SimboloCondicional : '='
                       | DIFFERENT
                       | LESSOREQUAL
                       | '<'
                       | GREATEROREQUAL
                       | '>'
    '''
    symbols = {
        '=': "EQUAL",
        '<>': "NEQ",
        '<=': "INFEQ",
        '<': "INF",
        '>=': "SUPEQ",
        '>': "SUP"
    }

    if len(p) == 2:
        symbol = p[1]
    else:
        symbol = p[1] + p[2]

    p[0] = symbols[symbol]
