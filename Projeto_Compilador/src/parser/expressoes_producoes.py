from symbol_table import generalSTable

# ====== Produções de Expressões ======

def p_Expressao_complex(p):
    '''
    Expressao : Expressao '+' Termo
              | Expressao '-' Termo
    '''
    left_val, left_type, left_code = p[1]
    right_val, right_type, right_code = p[3]
    op = p[2]

    if left_type != right_type:
        # print("Erro: tipos incompatíveis na expressão")
        p[0] = (None, "error", "")
        return

    op_code = "ADD" if op == '+' else "SUB"

    # ===== Constant folding =====
    if left_code == "" and right_code == "":
        result = left_val + right_val if op == '+' else left_val - right_val
        p[0] = (result, left_type, "")
    else:
        left_push = left_code if left_code else f"PUSHI {left_val}" if left_type == "integer" else f"PUSHF {left_val}"
        right_push = right_code if right_code else f"PUSHI {right_val}" if right_type == "integer" else f"PUSHF {right_val}"

        code = f"{left_push}\n{right_push}\n{op_code}"
        p[0] = (None, left_type, code)


def p_Expressao(p):
    '''
    Expressao : Termo
    '''
    p[0] = p[1]

    


def p_termo_complex(p):
    '''
    Termo : Termo '*' Fator
          | Termo MOD Fator
          | Termo DIV Fator
    '''
    left_val, left_type, left_code = p[1]
    right_val, right_type, right_code = p[3]
    op = p[2].lower()

    if left_type != right_type:
        # print("Erro: tipos incompatíveis no termo")
        p[0] = (None, "error", "")
        return

    op_map = {"*": "MUL", "mod": "MOD", "div": "DIV"}
    op_code = op_map[op]

    # ===== Constant folding =====
    if left_code == "" and right_code == "":
        if op == "*":
            result = left_val * right_val
        elif op == "mod":
            result = left_val % right_val
        elif op == "div":
            result = left_val // right_val
        p[0] = (result, left_type, "")
    else:
        # Emit code for known values
        left_push = left_code if left_code else f"PUSHI {left_val}" if left_type == "integer" else f"PUSHF {left_val}"
        right_push = right_code if right_code else f"PUSHI {right_val}" if right_type == "integer" else f"PUSHF {right_val}"

        code = f"{left_push}\n{right_push}\n{op_code}"
        p[0] = (None, left_type, code)


def p_termo_simple(p):
    '''
    Termo : Fator
    '''
    p[0] = p[1]


def p_fator_id(p):
    'Fator : ID'
    name = p[1]
    if not generalSTable.has_variable(name):

        p[0] = (p[1], "error", "")
    else:
        var_type = generalSTable.get_type(name)
        pos = generalSTable.get_position(name)

        if pos == -1:
            x = generalSTable.get_getter(p[1])
            p[0] = (p[1], var_type, f"\nPUSHFP\nLOAD {x}")

        else:
            p[0] = (p[1], var_type, f"\nPUSHG {pos}")
        



def p_fator_integer(p):
    '''
    Fator : INTEGER
    '''
    p[0] = (p[1], "integer", "") # Value tipo Codigo


def p_fator_real(p):
    '''
    Fator : REAL
    '''
    p[0] = (p[1], "real", "")


def p_fator_string(p):
    '''
    Fator : STRING
    '''
    p[0] = (p[1], "string", "")


def p_fator_true(p):
    '''
    Fator : TRUE
    '''
    p[0] = (1, "boolean", "")


def p_fator_false(p):
    '''
    Fator : FALSE
    '''
    p[0] = (0, "boolean", "")


def p_fator_parenthesis(p):
    '''
    Fator : '(' Expressao ')'
    '''
    p[0] = p[2]


def p_fator_array(p):
    '''
    Fator : Acesso_array
    '''
    destino = p[1]
    if isinstance(destino, tuple) and destino[0] == "array":
        _, base_type, array_name, index_code = destino
        code = f"{index_code}\nLOADN"
        p[0] = (array_name, base_type, code)
    else: 
        p[0] = p[1]



def p_fator_func_call(p):
    '''
    Fator : ChamadaFuncao
    '''
    p[0] = p[1]

