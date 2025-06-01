from symbol_table import generalSTable


# ====== Produções de Arrays ======

def p_acesso_array(p):
    '''
    Acesso_array : Variavel_array '[' Expressao ']'
    '''
    array_name = p[1]
    index_val, index_type, index_code = p[3]

    if not generalSTable.has_variable(array_name):
        print(f"Erro: variável '{array_name}' não declarada.")
        p[0] = (None, "error", "")
        return

    if not generalSTable.has_variable(array_name):
        print(f"Erro: variável '{array_name}' não declarada.")
        p[0] = (None, "error", "")
        return
    

    if generalSTable.is_array(array_name):
        access_code = ""

        if index_code == "":
                if index_type == "integer":
                    access_code = f"PUSHI {index_val}"
                else:
                    print(f"Tipo desconhecido '{index_type}'")
                    p[0] = ""
                    return
        else:
            access_code = index_code


        base_type = generalSTable.get_array_base_type(array_name)
        lower_bound = generalSTable.get_array_lower_bound(array_name)
        base_pos = generalSTable.get_position(array_name)

    # Código para calcular o índice real na stack: (índice - lower_bound) + base_pos
        access_code =  f"PUSHGP\nPUSHI {base_pos}\nPADD\n" + access_code + f"\nPUSHI {lower_bound}\nSUB"
    # Isto representa a instrução para LOAD/STORE
        p[0] = ("array", base_type, array_name, access_code)

    elif generalSTable.get_type(array_name) == "string":
        stack_pos = generalSTable.get_position(array_name)
        if generalSTable.current_state != "global":
            if stack_pos == -1:
                getter = generalSTable.get_getter(array_name)
                access_code = f"PUSHL {getter}" + index_code + "\nPUSHI 1\nSUB" + f"\nCHARAT"
            else:
                access_code = f"PUSHL {stack_pos}" + index_code + "\nPUSHI 1\nSUB" + f"\nCHARAT"
        else:
            access_code =  f"PUSHG {stack_pos}" + index_code + "\nPUSHI 1\nSUB" + f"\nCHARAT"
        p[0] = (array_name, generalSTable.get_type(array_name), access_code)

    else:
        print(f"Erro: '{array_name}' não é um array.")
        p[0] = (None, "error", "")
        return



def p_variavel_array(p):
    '''
    Variavel_array : ID
                   | Acesso_array
    '''
    p[0] = p[1]
